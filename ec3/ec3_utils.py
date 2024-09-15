import pgeocode


def postal_to_latlong(postal_code, country_code="US"):
    """
    Converts postal code to latitude and longitude returned as array.
    Refer to pgeocode documentation for supported country codes.
    If not found, then coordinates for Null Island are returned (0,0).

    Args:
        postal_code (int): postal code
        country_code (str, optional): Two letter country code. Defaults to 'US'.

    Returns:
        A tuple containing a float (latitude) and a float (longitude)
    """
    lat = 0
    long = 0
    nomi = pgeocode.Nominatim(country_code)
    if nomi:
        df = nomi.query_postal_code(str(postal_code))
        lat = df["latitude"].item()
        long = df["longitude"].item()
    return (lat, long)


def recursive_dict_list_return(dict_item, key_name, out_keys, outlist=[]):
    """
    Recursively loops through a nested json/dictionary based on the key name

    This is intended for where the key_name may occur at multiple levels of nesting.
    For example, the "subcategories" key occurs at multiple levels of the EC3 categories tree.
    Using this function allows you to return a flattened list of dictionaries with the
    desired keys defined in the "out_keys" argument.

    Args:
        dict_item (dict): Dictionary with nested data to crawl through
        key_name (str): Name of key to crawl through nested dictionary
        out_keys (list[str]): List of key names to return
        outlist (list, optional): List to return (can be left empty if starting a new list)

    Returns:
        list: List of dictionaries with keys provided in out_keys
    """
    if (key_name in dict_item.keys()) and dict_item[key_name]:
        new_dict = {k: dict_item[k] for k in out_keys}
        outlist.append(new_dict)

        for d in dict_item[key_name]:
            recursive_dict_list_return(d, key_name, out_keys, outlist=outlist)

    elif key_name in dict_item:
        new_dict = {k: dict_item[k] for k in out_keys}
        outlist.append(new_dict)

    return outlist


def get_masterformat_category_dict(category_tree):
    """
    Get a dictionary with masterformat codes as the keys and ids as the values

    Args:
        category_tree (dict): This should be a nested dictionary of all or part of the category tree

    Returns:
        dict: Dictionary with masterformat codes as keys (ex: {'03 00 00 Concrete': '484df282d43f4b0e855fad6b351ce006'})
    """
    category_dict_list = recursive_dict_list_return(
        category_tree, "subcategories", ["masterformat", "id"]
    )

    masterformat_dict = {i.get("masterformat"): i.get("id") for i in category_dict_list if i.get("masterformat") and i.get("id")}
    return masterformat_dict


def get_displayname_category_dict(category_tree):
    """
    Get a dictionary with display names as the keys and ids as the values

    Args:
        category_tree (dict): This should be a nested dictionary of all or part of the category tree

    Returns:
        dict: Dictionary with display names as keys (ex: {'Ready Mix': '6991a61b52b24e59b1244fe9dee59e9b'})
    """
    category_dict_list = recursive_dict_list_return(
        category_tree, "subcategories", ["display_name", "id"]
    )
    display_name_dict = {i.get("display_name"): i.get("id") for i in category_dict_list if i.get("display_name") and i.get("id")}
    return display_name_dict
