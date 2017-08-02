import re
from collections import defaultdict

### Regular Expression for a street name
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected_st_names = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Highway",
                     "Trail", "Parkway", "Commons"]

street_types = defaultdict(set)

# Mapping used to correct abbreviated street names
mapping = { '#204':'Avenue',
            'av': 'Avenue',
            'ave': 'Avenue',
            'blvd': 'Boulevard',
            'cl': 'Close',
            'ct': 'Court',
            'dr': 'Drive',
            'e': 'East',
            'gr': 'Grove',
            'hindry': 'Hindry Place',
            'hwy': 'Highway',
            'lp': 'Loop',
            'ln': 'Lane',
            'n': 'north',
            'ne': 'northeast',
            'north': 'North',
            'nw': 'Northwest',
            'park': 'Park',
            'pkwy': 'Parkway',
            'pl': 'Place',
            'rd': 'Road',
            's': 'South',
            'se': 'Southeast',
            'sq': 'Square',
            'sr': 'Drive',
            'st': 'Street',
            'ste': 'Suite',
            'sw': 'Southwest',
            'trl': 'Trail',
            'w': 'West'
          }


def audit_street_type(street_types, street_name):
    """
    Function to audit a street name type, and if street type is not in
    excepted list of streets, add it to a set
    :param street_types: Used to gather all the distinct street types that are not expected
    :param street_name: Street name saved in street types for reference
    :return None
    """
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_st_names:
            street_types[street_type].add(street_name)


def audit_streets(doc):
    """
    Function to audit Street types, and if street type is not in
    excepted list of streets, add it to a set.
    Return the street types that are not expected
    :param doc: XML document tree
    :return street_types: All the unexpected Street types with street names encounter parsing the data set
    """
    for element in doc.iter("tag"):
        k, v = element.attrib["k"], element.attrib["v"]
        if k.startswith("addr:street"):
            audit_street_type(street_types, v)
    return street_types


def clean_street_name(name):
    """
    Clean a street name according to mapping defined.
    Example :- Rd. will become Road, St. will become Street etc.
    :param name: Unexpected or abbreviated street name
    :return : Corrected Street name
    """
    s = name.split()[-1].lower().strip('.')
    name = name.split()[:-1] + [mapping[s]]
    return ' '.join(name)