from datetime import datetime

from .ec3_api import EC3Abstract
from .ec3_urls import EC3URLs
from .ec3_categories import EC3Categories
from .ec3_utils import postal_to_latlong, get_masterformat_category_dict


class EC3Materials(EC3Abstract):
    """
    Wraps functionality of EC3 Materials

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

        # NOTE "sort_by" is not currently working as expected when passing multiple fields.
        # Setting up to expect a single string field temporarily.
        if self.sort_by:
            params["params"]["sort_by"] = self.sort_by

        if self.only_valid:
            params["params"]["epd__date_validity_ends__gt"] = datetime.today().strftime(
                "%Y-%m-%d"
            )

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
