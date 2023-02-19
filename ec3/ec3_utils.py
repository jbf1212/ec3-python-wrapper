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
