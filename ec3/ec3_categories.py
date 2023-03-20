from .ec3_api import EC3Abstract
from .ec3_urls import EC3URLs


class EC3Categories(EC3Abstract):
    """
    Wraps functionality of EC3 Categories

    Usage:
        >>> ec3_categories = EC3Categories(bearer_token=token, ssl_verify=False)
        >>> ec3_categories.get_all_categories()
    """

    def __init__(self, bearer_token, response_format="json", ssl_verify=True):
        super().__init__(
            bearer_token, response_format=response_format, ssl_verify=ssl_verify
        )

        self.url = EC3URLs(response_format=response_format)

    def get_all_categories(self):
        """
        Gets the entire categories tree

        Returns:
            dict: Dictionary of entire category tree
        """
        return super()._request("get", self.url.categories_tree_url())

    def get_category_by_id(self, category_id):
        """
        Returns the category from a category id

        Args:
            category_id (str): Category ID

        Returns:
            dict: Returns a category by ID with the whole sub-categories tree
        """
        return super()._request(
            "get", self.url.categories_id_url().format(category_id=category_id)
        )
