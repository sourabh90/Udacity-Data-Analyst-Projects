import time
from audit_values import *


def audit_level_2_elements(doc, start_lat, end_lat, start_lon, end_lon, tolerance=0.005):
    """
    Function to audit level 2 elements(node, way, relation)
    and remove elements that do not conform to auditing
    :param doc: XML document
    :param start_lat : Lower limit of Latitude Boundary
    :param end_lat : Upper Limit of Latitude Boundary
    :param start_lon: Lower limit of Longitude Boundary
    :param end_lon: Upper limit of Longitude Boundary
    :param tolerance: Tolerance value for an object to be outside of the boundary
    :return: XML document object after auditing level 2 elements and invalid node references to remove
    """
    start = time.time()
    ids_to_clear = []
    id_list = {"node":[], "way":[], "relation":[]}

    for elem in doc.iter("node", "way", "relation"):
        remove_flag = False
        tag = elem.tag
        attr = elem.attrib

        id = attr["id"]
        version = attr["version"]
        timestamp = attr["timestamp"]
        changeset = attr["changeset"]
        uid = attr["uid"]

        if not audit_ID(id, id_list[tag]):
            remove_flag = True
        elif (tag == "node") and \
                (not (audit_latitude_longitude(attr["lat"], start_lat, end_lat, tolerance)\
                        and audit_latitude_longitude(attr["lon"], start_lon, end_lon, tolerance)\
                      )\
                 ):
            remove_flag = True
        elif not is_integer(version):
            remove_flag = True
        elif not is_datetime_TZ(timestamp):
            remove_flag = True
        elif not is_integer(changeset):
            remove_flag = True
        elif not is_integer(uid):
            remove_flag = True

        if remove_flag:
            ids_to_clear.append(id)
            tmp = elem
            elem = elem.getnext()
            tmp.getparent().remove(tmp)
        else :
            id_list[tag].append(id)

    print 'Time Taken :: ', round(time.time() - start, 3), " seconds"
    return doc, ids_to_clear


def clear_invalid_node_references(doc, ids_to_remove):
    """
    Function to remove bad node IDs from "nd" elements inside "way" element
    :param doc: XML document tree
    :param ids_to_remove: Invalid node references to remove
    :return Clean XML document tree after level 2 element auditing
    """
    start = time.time()
    for elem in doc.iter("nd"):
        ref = elem.attrib["ref"]

        if ref in ids_to_remove:
            tmp = elem
            elem = elem.getnext()
            tmp.getparent().remove(tmp)

    print 'Time Taken :: ', round(time.time() - start, 3), " seconds"
    return doc