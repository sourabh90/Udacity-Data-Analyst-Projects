# Functions that will help getting a summary of the XML document
import time


def sort(data, reverse=False):
    """
    This is a helper function that will sort a dictionary contents according to values in ASC or DESC order.
    :param data: Dictionary data to sort by values in given order
    :param reverse: True/False parameter to sort data in asc/desc order
    :return : returns a list of sorted dictionary keys
    """
    for key, value in data.items():
        return {key: [(kk, vv) for vv, kk in sorted([(v, k) for k, v in value.items()], reverse=reverse)]}


def gather_element_counts_levels(doc, tag_counts={}, tag_levels={}, attrib_counts={}):
    """
    This is a utility function that will recursively get the root element of the
    XML file and will find all the tags being used in the XML. It will
    find the level of each tag(root tag being at level 1), and also count
    the number of times the tags appeared.
    :param doc: Entire XML document
    :param tag_counts: A dictionary object representing tag counts
    :param tag_levels: A dictionary object representing level of each tag
    :param attrib_counts: A dictionary object representing attributes with respective counts
    :return: A list object containing the root element, tag counts, tag levels & attributes' counts
    """
    for elem in doc.iter():
        tag = elem.tag
        tag_counts[tag] = tag_counts.get(tag, 0) + 1

        for attr in elem.attrib:
            attr = tag + ':' + attr
            attrib_counts[attr] = attrib_counts.get(attr, 0) + 1

        i = 1
        for ancestor in elem.iterancestors():
            i += 1
        tag_levels[tag] = i
    return [{"root": doc.getroot().tag},
            {"tag_counts": tag_counts},
            {"tag_levels": tag_levels},
            {"attrib_counts": attrib_counts}]


def get_xml_stats(doc):
    """
    This function will gather basic statistics for the input XML file. This includes
    getting the root tag, and finding all the tags being used with the levels & counts.
    :param doc: Input OSM XML parsed document
    :return: dictionary containing basic statistics like tag counts, root tag etc.
    """
    start = time.time()
    data = gather_element_counts_levels(doc, {}, {}, {})

    data[1] = sort(data[1], reverse=True)
    data[2] = sort(data[2])
    data[3] = sort(data[3], reverse=True)

    print 'Run time to extract statistics :: {} seconds'.format(round(time.time() - start, 3))
    return data


def count_tag_keys(doc):
    """
    This function will count number of tag keys in the XML document.
    :param doc: XML doc object
    :return: dictionary containing basic statistics like tag counts, root tag etc.
    """
    keys = {}
    for elem in doc.iter("tag"):
        key = elem.attrib.get('k')
        if key:
            if key not in keys:
                keys[key] = 1
            else:
                keys[key] += 1
    return keys
