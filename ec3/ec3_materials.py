from datetime import datetime
import json

from .ec3_api import EC3Abstract
from .ec3_urls import EC3URLs
from .ec3_categories import EC3Categories
from .ec3_utils import postal_to_latlong, get_masterformat_category_dict


class EC3Materials(EC3Abstract):
    """
    Wraps functionality of EC3 Materials

    :ivar list return_fields: List of the fields you would like returned (EC3 returns everything by default), defaults to []
    :ivar str sort_by: Optional name of return field to sort results by, defaults to ""
    :ivar bool only_valid: If True will return only Materials with EPDs that are currently valid (set to False to also return materials with expired EPDs), defaults to True
    :ivar list masterformat_filter: Optional list of Masterformat Category names to filter by (ex: ["03 21 00 Reinforcement Bars"]), defaults to []

    Usage:
        >>> ec3_materials = EC3Materials(bearer_token=token, ssl_verify=False)
        >>> ec3_mat_list = ec3_materials.get_materials(params=mat_param_dict)
    """

    def __init__(self, bearer_token, response_format="json", ssl_verify=True):
        super().__init__(
            bearer_token, response_format=response_format, ssl_verify=ssl_verify
        )

        self.return_fields = []
        self.sort_by = ""
        self.only_valid = True
        self.masterformat_filter = (
            []
        )  # Currently EC3 requires you to go through category class for this

        self.url = EC3URLs(response_format=response_format)

    def _process_params(self, params):
        params["params"]["page_size"] = self.page_size

        if self.return_fields:
            fields_string = ",".join(self.return_fields)
            params["params"]["fields"] = fields_string

            # FIXME seems like this is not return full dictionaries for nested values

        # NOTE "sort_by" is not currently working as expected when passing multiple fields.
        # Setting up to expect a single string field temporarily.
        if self.sort_by:
            params["params"]["sort_by"] = self.sort_by

        if self.masterformat_filter:
            ec3_categories = EC3Categories(
                bearer_token=self.bearer_token, ssl_verify=False
            )
            whole_tree = ec3_categories.get_all_categories()
            masterformat_dict = get_masterformat_category_dict(whole_tree)

            category_ids = [masterformat_dict[i] for i in self.masterformat_filter]
            params["params"]["category"] = category_ids

        return params

    def get_materials(self, return_all=False, **params):
        """
        Returns matching materials

        Args:
            return_all (bool, optional): Set to True to return all matches. Defaults to False, which will return the quantity specified in max_records.

        Returns:
            list: List of dictionaries of matching material records
        """
        if self.only_valid:
            params["params"]["epd__date_validity_ends__gt"] = datetime.today().strftime(
                "%Y-%m-%d"
            )

        processed_params = self._process_params(params)

        if return_all:
            return super()._get_all(self.url.materials_url(), **processed_params)
        else:
            return super()._get_records(self.url.materials_url(), **processed_params)

    def convert_query_to_mf_string(self, category_name, field_dict_list, pragma=None):
        """
        Converts a dictionary of material search parameters to a pragma string for use in the EC3 API
        This function includes a POST request that requires an API key with write access

        Args:
            category_name (str): EC3 category name (see https://docs.open-epd-forum.org/en/data-format/materials/ for list of valid category names)
            field_dict_list (list): List of dictionaries of search parameters (format: [{"field": "field_name", "op": "operator", "arg": "argument"}])
            pragma (list, optional): List of dictionaries of pragma parameters. Defaults to eMF 2.0/1 and TRACI 2.1.

        Returns:
            str: string formatted to work with MaterialFilter pragma in EC3 API
        """
        payload_dict = {}

        if pragma is None:
            pragma = [
                {"name": "eMF", "args": ["2.0/1"]},
                {"name": "lcia", "args": ["TRACI 2.1"]},
            ]

        payload_dict["pragma"] = pragma
        payload_dict["category"] = category_name
        payload_dict["filter"] = field_dict_list

        payload = json.dumps(payload_dict)

        mf_url = (
            self.url.materials_convert_matfilter_url()
            + "?output=string&output_style=compact"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bearer_token}",
        }
        response = self.session.request(
            "post", mf_url, verify=self._ssl_verify, data=payload, headers=headers
        )

        return response

    def get_materials_mf(self, category_name, mf_list, return_all=False, **params):
        """
        Returns matching materials using filters

        Args:
            category_name (str): Open EPD category name (see https://docs.open-epd-forum.org/en/data-format/materials/ for list of valid category names)
            mf_list (list): List of dictionaries of search parameters (format: [{"field": "field_name", "op": "operator", "arg": "argument"}])
            return_all (bool, optional): Set to True to return all matches. Defaults to False, which will return the quantity specified in max_records.

        Returns:
            list: List of dictionaries of matching material records
        """
        if self.only_valid:
            mf_list.append(
                {
                    "field": "epd__date_validity_ends",
                    "op": "gt",
                    "arg": datetime.today().strftime("%Y-%m-%d"),
                }
            )

        mf_response = self.convert_query_to_mf_string(category_name, mf_list)
        mf_response_json = mf_response.json()
        mf_string = mf_response_json["material_filter_str"]

        params["params"] = {}
        params["params"]["mf"] = mf_string

        processed_params = self._process_params(params)

        if return_all:
            return super()._get_all(self.url.materials_url(), **processed_params)
        else:
            return super()._get_records(self.url.materials_url(), **processed_params)

    def get_materials_within_region(
        self,
        postal_code,
        country_code="US",
        plant_distance="100 mi",
        return_all=False,
        **params,
    ):
        """
        Returns only materials from plants within provided distance of postal code.
        This adds the "latitude", "longitude", and "plant_distance_lt" keys to your parameter dictionary.

        Args:
            postal_code (int): postal code
            country_code (str, optional): Two letter country code.. Defaults to 'US'.
            plant_distance (str, optional): Distance to plant with units in string ('mi' or 'km'). Defaults to "100 mi".
            return_all (bool, optional): Set to True to return all matches. Defaults to False, which will return the quantity specified in max_records.

        Returns:
            list: List of dictionaries of matching material records within distance provided from postal code
        """
        lat, long = postal_to_latlong(postal_code, country_code)
        params["params"]["latitude"] = lat
        params["params"]["longitude"] = long
        params["params"]["plant__distance__lt"] = plant_distance

        return self.get_materials(return_all=return_all, **params)

    def get_materials_within_region_mf(
        self,
        category_name,
        mf_list,
        postal_code,
        country_code="US",
        plant_distance="100 mi",
        return_all=False,
        **params,
    ):
        """
        Returns only materials from plants within provided distance of postal code.
        This adds the "latitude", "longitude", and "plant_distance_lt" keys to your parameter dictionary.

        Args:
            category_name (str): Open EPD category name (see https://docs.open-epd-forum.org/en/data-format/materials/ for list of valid category names)
            mf_list (list): List of dictionaries of search parameters (format: [{"field": "field_name", "op": "operator", "arg": "argument"}])
            postal_code (int): postal code
            country_code (str, optional): Two letter country code.. Defaults to 'US'.
            plant_distance (str, optional): Distance to plant with units in string ('mi' or 'km'). Defaults to "100 mi".
            return_all (bool, optional): Set to True to return all matches. Defaults to False, which will return the quantity specified in max_records.

        Returns:
            list: List of dictionaries of matching material records within distance provided from postal code
        """
        lat, long = postal_to_latlong(postal_code, country_code)

        mf_list.extend(
            [
                {"field": "latitude", "op": "exact", "arg": lat},
                {"field": "longitude", "op": "exact", "arg": long},
                {"field": "plant__distance", "op": "lt", "arg": plant_distance},
            ]
        )

        return self.get_materials_mf(
            category_name, mf_list, return_all=return_all, **params
        )

    # NOTE Querying materials by "open_xpd_uuid" does not appear to currently work with the api
    # def get_material_by_xpduuid(self, epd_xpd_uuid):
    #     """
    #     Returns the material from an Open xPD UUID of an EPD

    #     Args:
    #         epd_xpd_uuid (str): Open xPD UUID (Example: EC300001)

    #     Returns:
    #         list: List of dictionaries of matching material records
    #     """
    #     return super()._request(
    #         "get", self.url.materials_xpd_uuid_url().format(epd_xpd_uuid=epd_xpd_uuid)
    #     )
