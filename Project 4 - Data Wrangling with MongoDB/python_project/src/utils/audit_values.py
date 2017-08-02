import re
from datetime import datetime


def almost_within(num, lower, upper, tolerance):
    """
    Function that will check if a numeric value(num) is within an interval[lower, upper] or
    not with some provided tolerance.
    :param num: Number to check
    :param lower: Lower limit
    :param upper: Upper Limit
    :param tolerance: Tolerance value used to modify the boundaries
    :return True/False: If number is withing the boundaries(with tolerance)
    """
    return lower-tolerance <= num <= upper+tolerance


def is_integer(x):
    """
    This is a helper function used to find out if a number is integer or not
    :param x: String to check if it is an integer or not
    :return True/False
    """
    try:
        x = int(x)
        return True
    except ValueError:
        return False


def is_float(x):
    """
    This is a helper function used to find out if a number is float or not
    :param x: String to check if it is an float or not
    :return True/False
    """
    try:
        x = float(x)
        return True
    except ValueError:
        return False


def is_datetime_TZ(t):
    """
    This is a helper function used to find out if a number is valid timestamp or not
    :param t: String to check if it is an valid timestamp or not
    :return True/False
    """
    try:
        t = datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False


def audit_ID(ID, ID_LIST):
    """
    Function to audit the ID fields of node, way & relation elements
    :param ID: Node, Way or Relation ID field from XML
    :param ID_LIST: List of IDs already present, used to check for duplicates
    :return True/False
    """
    if ID in ID_LIST:
        print 'Duplicate {} ID'.format(type)
        return False
    else:
        return is_integer(ID)


def audit_latitude_longitude(value, start, end, tolerance):
    """
    Function to audit the Latitude & Longitude fields.
    Also it will check if the lat & lon is within bounds with a defined tolerance of 0.005.
    :param value: Latitude or Longitude value
    :param start: Lower Boundary
    :param end: Upper Boundary
    :param tolerance: Tolerance value while checking lat & lon within the boundaries
    :return True/False
    """
    r = False
    if is_float(value):
        value = float(value)
        if almost_within(value, start, end, tolerance):
            r = True

    return r


def audit_postcode(postcode):
    """
    Function to audit the postcode values.
    :param postcode: Postcode value
    :return True/False
    """
    r = False
    us_postcode_format = re.compile("^\d{5}$")
    if us_postcode_format.match(postcode):
        r = True

    return r
