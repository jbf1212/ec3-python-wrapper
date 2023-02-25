import abc
import requests


class EC3Abstract(metaclass=abc.ABCMeta):
    """
    Represents the abstract class for the Building Transparency Api

    This class get inherited by other major classes.
    """

    def __init__(self, bearer_token, response_format="json", ssl_verify=True):
        """
        Args:
            bearer_token (str): EC3 bearer token for the user
            response_format (str, optional): Defaults to "json".
            ssl_verify (bool, optional): Defaults to True.
        """

        session = requests.Session()
        self.session = session
        self.session.headers.update({"Authorization": "Bearer {}".format(bearer_token)})

        self.page_size = 100  # Specifies the page size to return. Default is 100. Max allowed by api is 250
        self.max_records = 100  # Specifies the maximum number of records to return.

        self.format = response_format
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # ignore any unresolved references
            requests.packages.urllib3.disable_warnings()

        self.remove_nulls = True  # Determines if responses should return items with null values since EC3 returns everything

    def _process_response(self, response):
        """
        Processes the response. Removes null values if set to do so.

        Args:
            response (requests.models.Response): response from Api

        Returns:
            json: Processed records as json
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            err_msg = str(exc)

            # Attempt to get Error message from response
            try:
                error_dict = response.json()
            except ValueError:
                pass
            else:
                if "error" in error_dict:
                    err_msg += " [Error: {}]".format(error_dict["error"])
            exc.args = (*exc.args, err_msg)
            raise exc
        else:
            # if user put in anything other than True or False, assume True
            if type(self.remove_nulls) != bool:
                self.remove_nulls = True

            if self.remove_nulls is True:
                ec3_response = response.json()
                if isinstance(ec3_response, dict):
                    cleaned_response = self._remove_nulls(ec3_response)
                else:
                    cleaned_response = [self._remove_nulls(d) for d in ec3_response]
                return cleaned_response
            else:
                return response.json()

    def _request(self, method, url, params=None):
        if params:
            response = self.session.request(
                method, url, verify=self._ssl_verify, params=params["params"]
            )
        else:
            response = self.session.request(method, url, verify=self._ssl_verify)

        return self._process_response(response)

    def _get_records(self, url, **params):
        """
        Returns the requested number of records.

        This will only return the first (or specified #) page when number of records exceeds page size.
        """
        data = self._request("get", url, params=params)
        requested_records = data
        page_number = 1

        while len(data) == self.page_size and len(requested_records) < self.max_records:
            page_number += 1
            params["params"]["page_number"] = page_number

            try:
                data = self._request("get", url, params=params)
            except requests.exceptions.HTTPError:
                break

            if data:
                requested_records.extend(data)

        if len(requested_records) > self.max_records:
            return requested_records[0 : self.max_records]
        else:
            return requested_records

    def _get_all(self, url, **params):
        """
        Returns all the records as a single list
        """
        hold_val1 = self.max_records
        self.max_records = 10000000  # temp max value

        data = self._get_records(url, **params)
        all_records = data
        page_number = 1

        while len(data) == self.page_size:
            page_number += 1
            params["params"]["page_number"] = page_number

            try:
                data = self._get_records(url, **params)
            except requests.exceptions.HTTPError:
                break

            if data:
                all_records.extend(data)

        self.max_records = hold_val1

        return all_records

    def _remove_nulls(self, response_dict):
        """
        Removes key/value pairs where value is None

        Args:
            response_dict (dict): Response dictionary

        Returns:
            dict: Cleaned version of input dictionary
        """
        for key, value in list(response_dict.items()):
            if value is None:
                del response_dict[key]
            elif isinstance(value, dict):
                self._remove_nulls(value)
        return response_dict
