class EC3URLs:
    """
    This class is intended to store commonly used EC3 URLs.
    Should EC3 URLs change in the future they can be updated here
    """

    def __init__(self, response_format="json"):
        self.format = response_format

        self.base_url = "https://buildingtransparency.org/api/"

        # materials
        self.materials = "materials"
        self.material_statistics = "materials/statistics.{format}".format(
            format=self.format
        )
        self.material_statistics_cached = "materials/statistics/cached.{format}".format(
            format=self.format
        )
        self.material_epds_xpd_uuid = "materials?open_xpd_uuid={epd_xpd_uuid}".format(
            epd_xpd_uuid="{epd_xpd_uuid}"
        )

        # epds
        self.epds = "epds"
        self.epds_xpd_uuid = "epds/{epd_xpd_uuid}".format(
            format=self.format, epd_xpd_uuid="{epd_xpd_uuid}"
        )
        self.epds_id = "epds/{id}.{format}".format(format=self.format, id="{id}")

        # projects
        self.projects = "projects"
        self.projects_id = "projects?id={project_id}".format(
            format=self.format, project_id="{project_id}"
        )
        self.projects_name = "projects?name__like={project_name}".format(
            format=self.format, project_name="{project_name}"
        )

        # categories
        self.categories_tree = "categories/root"
        self.categories_id = "categories/{category_id}".format(
            format=self.format, category_id="{category_id}"
        )

    def base_url(self):
        """
        Returns the base url
        """
        return self.base_url

    ### MATERIALS ###
    def materials_url(self):
        """
        Combines the base URL and materials API URL
        """
        return self.base_url + self.materials

    def material_statistics_url(self):
        """
        Combines the base URL and materials statistics API URL
        """
        return self.base_url + self.material_statistics

    def material_statistics_cached_url(self):
        """
        Combines the base URL and materials statistics cached API URL
        """
        return self.base_url + self.material_statistics_cached

    def materials_xpd_uuid_url(self):
        """
        Combines the base URL and epds_xpd_uuid API URL
        """
        return self.base_url + self.material_epds_xpd_uuid

    ### EPDs ###
    def epds_url(self):
        """
        Combines the base URL and epds API URL
        """
        return self.base_url + self.epds

    def epds_xpd_uuid_url(self):
        """
        Combines the base URL and epds_xpd_uuid API URL
        """
        return self.base_url + self.epds_xpd_uuid

    def epds_id_url(self):
        """
        Combines the base URL and epds_id API URL
        """
        return self.base_url + self.epds_id

    def epds_product_classes_url(self):
        """
        Combines the base URL and epds_id API URL
        """
        return self.base_url + self.product_classes

    ### PROJECTS ###
    def projects_url(self):
        """
        Combines the base URL and projects API URL
        """
        return self.base_url + self.projects

    def projects_id_url(self):
        """
        Combines the base URL and projects ID API URL
        """
        return self.base_url + self.projects_id

    def projects_name_url(self):
        """
        Combines the base URL and projects ID API URL
        """
        return self.base_url + self.projects_name

    ### CATEGORIES ###
    def categories_tree_url(self):
        """
        Combines the base URL and categories url for the whole categories tree
        """
        return self.base_url + self.categories_tree

    def categories_id_url(self):
        """
        Combines the base URL and projects ID API URL
        """
        return self.base_url + self.categories_id
