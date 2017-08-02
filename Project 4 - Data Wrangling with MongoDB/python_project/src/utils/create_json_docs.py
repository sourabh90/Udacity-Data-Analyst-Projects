import time, os
from collections import OrderedDict
import json
import codecs
from bson import json_util

from shape_xml_element import shape_element


def create_json_docs(doc):
    """
    Function to convert the entire XML document into a list of
    dictionary items(documents). These list will be used to create
    a JSON file that in turn will get loaded into Mongo DB
    :param doc: XML document Tree
    :return : Set of JSON dictionary documents converted from XML
    """
    start = time.time()
    data = []

    for element in doc.iter("node", "way"):
        el = shape_element(element)

        for key, value in el.items():
            if type(value) == OrderedDict:
                for k, v in value.items():
                    if k != "timestamp" and len(v) == 0:
                        del el[key][k]

            if len(value) == 0:
                    del el[key]

        data.append(el)

    print 'Time Taken :: ', round(time.time() - start, 3), " seconds"
    return data


def create_json_file(file_in, data, pretty = False):
    """
    Function to load all the JSON documents(dictionary list) into a JSON file.
    This file will get imported into Mongo DB using mongoimport command.
    :param file_in: Input XML file name that will be used to add .json at the tail
    :param data: List of dictionary documents
    :param pretty: Documents will be written prettily in JSON file if TRUE
    :return : None
    """

    start = time.time()
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    print 'Writing data to JSON file --- \n', file_out

    with codecs.open(file_out, "w") as fo:
        for node in data:
            if node:
                if pretty:
                    fo.write(json.dumps(node, indent=2, default=json_util.default)+"\n")
                else:
                    fo.write(json.dumps(node, default=json_util.default) + "\n")

    print "JSON file done."
    print 'File Size :: {} MB'.format(round(os.path.getsize(file_out) / (1024.0 * 1024), 3) )
    print 'Time Taken :: ', round(time.time() - start, 3), " seconds"