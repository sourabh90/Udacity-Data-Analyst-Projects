import re

### Regular Expressions to check Tag key character types
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    """
    Function to check key attribute of a Tag element
    :param element: An XML element object
    :param keys: Set of TAG element Key texts
    :return : Updated set of TAG element keys
    """
    k = element.attrib["k"]

    if re.search(lower, element.attrib['k']):
        keys['lower'] += 1
    elif re.search(lower_colon, element.attrib['k']):
        keys['lower_colon'] += 1
    elif re.search(problemchars, element.attrib['k']):
        keys['problemchars'] += 1
        # print out any values with problematic characters
        print element.attrib['k']
    else:
        keys['other'] += 1

    return keys


def audit_tag_keys(doc):
    """
    Function to audit key attributes of all XML Tag elements to check if we have any problem key texts
    :param doc: XML document tree
    :return : All TAG keys according to string characteristics
    """
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for element in doc.iter("tag"):
        keys = key_type(element, keys)

    return keys
