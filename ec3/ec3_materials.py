"""
The EC3Materials class is meant to simplify the querying of materials from the EC# database

The primary method currently setup for this class is the 'get_materials' method.
When using this the user should pass a dictionary of parameters and values for querying.

There are a large number of fields listed in the EC3 documentation that
can be used to query materials. Users should refer to that documentation
for the field names and values expected.

A small number of commonly used fields have been built into the class.
Refer to documentation below to see further details.
"""

from datetime import datetime

from .ec3_api import EC3Abstract
from .ec3_urls import EC3URLs


class EC3Materials(EC3Abstract):
    """
    Wraps functionality of EC3 Materials

    Usage:
        >>> ec3_mat_list = EC3Materials(bearer_token=token, ssl_verify=False)
        >>> ec3_mat_list.get_materials(params=mat_param_dict)
    """

    def __init__(self, bearer_token, response_format="json", ssl_verify=True):
        super().__init__(
            bearer_token, response_format=response_format, ssl_verify=ssl_verify
        )

        self.return_fields = []
        self.sort_by = ""
        self.only_valid = True

        self.url = EC3URLs(response_format=response_format)

    def _process_params(self, params):
        params["params"]["page_size"] = self.page_size

        if self.return_fields:
            fields_string = ",".join(self.return_fields)
            params["params"]["fields"] = fields_string

        # NOTE "sort_by" is not currently working as expected when passing multiple fields.
        # Setting up to expect a single string field temporarily.
        if self.sort_by:
            params["params"]["sort_by"] = self.sort_by

        if self.only_valid:
            params["params"]["epd__date_validity_ends__gt"] = datetime.today().strftime(
                "%Y-%m-%d"
            )

        return params

    def get_materials(self, return_all=False, **params):
        """
        Returns matching materials

        Args:
            return_all (bool, optional): Set to True to return all matches. Defaults to False, which will return the quantity specified in page_size.

        Returns:
            list: List of dictionaries of matching material records
        """
        processed_params = self._process_params(params)

        if return_all:
            return super()._get_all(self.url.materials_url(), **processed_params)
        else:
            return super()._get_records(self.url.materials_url(), **processed_params)

    def get_material_by_xpduuid(self, epd_xpd_uuid):
        """
        Returns the material from an Open xPD UUID of an EPD

        Args:
            epd_xpd_uuid (str): Open xPD UUID (Example: EC300001)
        """
        return super()._request(
            "get", self.url.materials_xpd_uuid_url().format(epd_xpd_uuid=epd_xpd_uuid)
        )
