"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
# mapping = {'ave': 'Avenue',
#            'Ave': 'Avenue',
#            'Ave.': 'Avenue',
#            'Blvd': 'Boulevard',
#            "blvd":"Boulevard",
#            'Broadway': 'Broadway',
#            'Bypass': 'Bypass',
#            'Centre': 'Centre',
#            'Close': 'Close',
#            'Crescent': 'Crescent',
#            'Diversion': 'Diversion',
#            'Dr': 'Drive',
#            'Dr.': 'Drive',
#            'East': 'East',
#            'Edmonds': 'Edmonds Street',
#            'Gate': 'Gate',
#            'Grove': 'Grove',
#            'Hastings': 'Hastings Street',
#            'Highway': 'Highway',
#            'Hwy': 'Highway',
#            'Hwy.': 'Highway',
#            'Kingsway': 'Kingsway',
#            'Mall': 'Mall',
#            'Mews': 'Mews',
#            'Moncton': 'Moncton Street',
#            'North': 'North',
#            'Park': 'Park',
#            'Pender': 'Pender Street',
#            'RD': 'Road',
#            'Rd': 'Road',
#            'Rd.': 'Road',
#            'Road,': 'Road',
#            'S.': 'South',
#            'Sanders': 'Sanders Street',
#            'South': 'South',
#            'St': 'Street',
#            'St.': 'Street',
#            'Street3': 'Street',
#            'Terminal': 'Terminal',
#            'Tsawwassen': 'North Tsawwassen',
#            'Vancouver': 'Vancouver',
#            'Walk': 'Walk',
#            'Way': 'Way',
#            'West': 'West',
#            'Willingdon': 'Willingdon',
#            'Wynd': 'Wynd',
#            'av': 'Avenue',
#            'road': 'Road',
#            'st': 'Street',
#            'street': 'Street',
#             "pl": "Place",
#             "st": "Street",
#             "ave": "Avenue",
#             "w": "West",
#             "n": "North",
#             "s": "South",
#             "e": "East",
#             "sr": "Drive",
#             "ct": "Court",
#             "ne": "Northeast",
#             "se": "Southeast",
#             "nw": "Northwest",
#             "sw": "Southwest",
#             "dr": "Drive",
#             "sq": "Square",
#             "ln": "Lane",
#             "rd": "Road",
#             "trl": "Trail",
#             "pkwy": "Parkway",
#             "ste": "Suite",
#             "lp": "Loop",
#             "hwy": "Highway",
#             "cmn": "Commons",
#             "cmns": "Commons"
# }


mapping = {
            '#204':'Avenue',
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
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return elem.attrib['k'] == "addr:street"


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, name_mappings):

    # YOUR CODE HERE
    s = name.split()[-1].lower().strip('.')
    name = name.split()[:-1] + [name_mappings[s]]
    return ' '.join(name)


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()
