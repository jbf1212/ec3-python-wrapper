from datetime import datetime

from .ec3_api import EC3Abstract
from .ec3_urls import EC3URLs
from .ec3_categories import EC3Categories
from .ec3_utils import get_masterformat_category_dict, get_displayname_category_dict


class EC3epds(EC3Abstract):
    """
    Wraps functionality of EC3 EPDs

    :ivar list return_fields: List of the fields you would like returned (EC3 returns everything by default), defaults to []
    :ivar str sort_by: Optional name of return field to sort results by, defaults to ""
    :ivar bool only_valid: If True will return only EPDs that are currently valid (set to False to also return expired EPDs), defaults to True
    :ivar list masterformat_filter: Optional list of Masterformat Category names to filter by (ex: ["03 21 00 Reinforcement Bars"]), defaults to []
    :ivar list display_name_filter: Optional list of Display Name Categories to filter by (ex: ["Ready Mix"]), defaults to []

    Usage:
        >>> ec3_epds = EC3epds(bearer_token=token, ssl_verify=False)
        >>> ec3_epd_list = ec3_epds.get_epds(params=epd_param_dict)
    """

    def __init__(self, bearer_token, response_format="json", ssl_verify=True):
        super().__init__(
            bearer_token, response_format=response_format, ssl_verify=ssl_verify
        )

        self.return_fields = []
        self.sort_by = ""
        self.only_valid = True
        self.category_tree = None
        self.masterformat_filter = (
            []
        )  # Currently EC3 requires you to go through category class for this
        self.display_name_filter = []

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
            params["params"]["date_validity_ends__gt"] = datetime.today().strftime(
                "%Y-%m-%d"
            )

        if self.masterformat_filter or self.display_name_filter:
            ec3_categories = EC3Categories(
                bearer_token=self.bearer_token, ssl_verify=False
            )
            self.category_tree = ec3_categories.get_all_categories()

        if self.masterformat_filter:
            masterformat_dict = get_masterformat_category_dict(self.category_tree)

            category_ids = [masterformat_dict[i] for i in self.masterformat_filter]
            params["params"]["category"] = category_ids

        if self.display_name_filter:
            display_name_dict = get_displayname_category_dict(self.category_tree)

            category_ids = [display_name_dict[i] for i in self.display_name_filter]
            category_ids = list(set(category_ids))  # Remove duplicates
            params["params"]["category"] = category_ids

        return params

    def get_epds(self, return_all=False, **params):
        """
        Returns matching EPDs

        Args:
            return_all (bool, optional): Set to True to return all matches. Defaults to False, which will return the quantity specified in page_size.

        Returns:
            list: List of dictionaries of matching EPD records
        """
        processed_params = self._process_params(params)

        if return_all:
            return super()._get_all(self.url.epds_url(), **processed_params)
        else:
            return super()._get_records(self.url.epds_url(), **processed_params)

    def get_epd_by_xpduuid(self, epd_xpd_uuid):
        """
        Returns the epd from an Open xPD UUID

        Args:
            epd_xpd_uuid (str): Open xPD UUID (Example: EC300001)
        Returns:
            dict: Dictionary of the matching EPD record
        """
        return super()._request(
            "get", self.url.epds_xpd_uuid_url().format(epd_xpd_uuid=epd_xpd_uuid)
        )
