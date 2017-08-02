from collections import defaultdict, OrderedDict
from datetime import datetime as dt
from audit_street_names import *
from audit_values import *
from tag_key_types import *

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
TAG_KEYS = ["amenity", "cuisine", "name", "phone", "website"]


def shape_element(element):
    """
    Function to convert an XML element into predefined data model dictionary(document)
    :param element: A single XML element Object
    :return : Dictionary item that will become a JSON/Mongo document
    """
    CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
    ADDRESS_ITEMS = ["housenumber", "street", "city", "state", "postcode"]

    node = OrderedDict({})

    node["_id"] = ""
    node["type"] = element.tag
    node["created"] = OrderedDict()
    node["pos"] = ""
    node["address"] = OrderedDict()
    node["amenity"] = ""
    node["cuisine"] = ""
    node["name"] = ""
    node["phone"] = ""
    node["website"] = ""
    node["node_refs"] = []

    for key in node.keys():
        if key == "created":
            for k in CREATED:
                node[key][k]= ""

        if key == "address":
            for k in ADDRESS_ITEMS:
                node[key][k] = ""

    attrs = element.attrib
    lat = None
    lon = None

    for attr in attrs:
        if attr == "id":
            node["_id"] = attrs[attr]
        elif attr in CREATED:
            if attr == "timestamp":
                node["created"][attr] = dt.strptime(attrs[attr], "%Y-%m-%dT%H:%M:%SZ")
            else:
                node["created"][attr] = attrs[attr]
        elif attr == "lat":
            lat = float(attrs[attr])
        elif attr == "lon":
            lon = float(attrs[attr])
        else:
            node[attr] = attrs[attr]

    if lat:
        node["pos"] = [lat] + [lon]

    for child in element:
        if child.tag == "nd":
            node["node_refs"] = node.get("node_refs", []) + [int(child.attrib["ref"])]
        else:
            k, v = child.attrib["k"], child.attrib["v"]

            if problemchars.match(k):
                # Skip tag if key is having invalid characters
                continue

            if k.startswith("addr") and k.count(":") == 1:
                node["address"] = node.get("address", {})

                if "housenumber" in k:
                    node["address"]["housenumber"] = v

                elif "street" in k:
                    street_name_tail = v.split()[-1].lower().strip(".'!@#$%^&*(){}\|;/<>'")

                    if is_integer(street_name_tail):
                        print "Street Name --- {}".format(v)
                        v = ' '.join(v.split()[:-1])
                        street_name_tail = v.split()[-1].lower().strip(".'!@#$%^&*(){}\|;/<>'")

                    if street_name_tail in mapping.keys():
                        node["address"]["street"] = clean_street_name(v)
                        print "Street Name corrected --- {} ==> {}".format(v, node["address"]["street"])
                    else:
                        node["address"]["street"] = v

                elif "city" in k:
                    node["address"]["city"] = v

                elif "state" in k:
                    node["address"]["state"] = v

                elif "postcode" in k:
                    if audit_postcode(v):
                        node["address"]["postcode"] = v

            else:
                if k in TAG_KEYS:
                    node[k] = v

    return node
