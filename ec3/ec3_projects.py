from .ec3_api import EC3Abstract
from .ec3_urls import EC3URLs


class EC3Projects(EC3Abstract):
    """
    Wraps functionality of EC3 Projects

    Usage:
        >>> ec3_project_list = EC3Projects(bearer_token=token, ssl_verify=False)
        >>> ec3_project_list.get_projects(params=project_param_dict)
    """

    def __init__(self, bearer_token, response_format="json", ssl_verify=True):
        super().__init__(
            bearer_token, response_format=response_format, ssl_verify=ssl_verify
        )

        self.sort_by = ""

        self.url = EC3URLs(response_format=response_format)

    def _process_params(self, params):
        params["params"]["page_size"] = self.page_size

        # NOTE "sort_by" is not currently working as expected when passing multiple fields.
        # Setting up to expect a single string field temporarily.
        if self.sort_by:
            params["params"]["sort_by"] = self.sort_by

        return params

    def get_projects(self, return_all=False, **params):
        """
        Returns matching Projects in your EC3 account

        Args:
            return_all (bool, optional): Set to True to return all matches. Defaults to False, which will return the quantity specified in page_size.

        Returns:
            list: List of dictionaries of matching Project records
        """
        processed_params = self._process_params(params)

        if return_all:
            return super()._get_all(self.url.projects_url(), **processed_params)
        else:
            return super()._get_records(self.url.projects_url(), **processed_params)

    def get_project_by_id(self, project_id):
        """
        Returns the project from a project id

        Args:
            project_id (str): Entity ID
        """
        return super()._request(
            "get", self.url.projects_id_url().format(project_id=project_id)
        )

    def get_projects_by_name(self, project_name):
        """
        Returns a list of projects with a name equivalent to the input
        If your exact project name is put here you should get a list with one item.

        Args:
            project_name (str): Search term for your EC3 project name
        """
        return super()._request(
            "get", self.url.projects_name_url().format(project_name=project_name)
        )
