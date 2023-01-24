"""
The EC3Abstract class is an abstract class that contains some of the functionality
used across some of the other classes that inherit from it.

This is currently built primarily for retrieving data from EC3.
Future development may focus on other capabilities to manage and upload data.

Full api documentation can be found at:
https://buildingtransparency.org/ec3/manage-apps/api-doc/api#/
"""
import abc
import requests


class EC3Abstract(metaclass=abc.ABCMeta):
    def __init__(self, bearer_token, response_format="json", ssl_verify=True):

        session = requests.Session()
        self.session = session
        self.session.headers.update({"Authorization": "Bearer {}".format(bearer_token)})

        self.page_size = 100  # specifies the max number of objects to return if not retrieving all (max allowed by api is 250)

        self.format = response_format
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # ignore any unresolved references
            requests.packages.urllib3.disable_warnings()

        self.remove_nulls = True  # Determines if responses should return items with null values since EC3 returns everything

    def _process_response(self, response):
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
        return self._request("get", url, params=params)

    def _get_all(self, url, **params):
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
