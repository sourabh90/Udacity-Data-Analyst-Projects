from utils import download_osm_data
from utils import get_xml_stats
from utils import count_tag_keys
from utils import audit_level_2_elements, clear_invalid_node_references
from utils import audit_tag_keys
from utils import create_json_docs, create_json_file

from mongops import *

import os
import time
from lxml import etree as le
from pprint import pprint


# Define Run Parameters
# ---------------------
# Latitude boundaries
SAMPLE_START_LAT = 33.85
SAMPLE_END_LAT = 33.86

START_LAT = 33.85
END_LAT = 33.88

# Longitude boundaries
SAMPLE_START_LON = -118.40
SAMPLE_END_LON = -118.37

START_LON = -118.40
END_LON = -118.35

# Overpass API URL
SAMPLE_URL = 'http://overpass-api.de/api/map?bbox={},{},{},{}'.format(
    SAMPLE_START_LON, SAMPLE_START_LAT, SAMPLE_END_LON, SAMPLE_END_LAT
)

URL = 'http://overpass-api.de/api/map?bbox={},{},{},{}'.format(START_LON, START_LAT, END_LON, END_LAT)

# File details to save map data
DIR = '../files'
sample_filename = 'sample.osm'
SAMPLE_FILENAME = os.path.join(DIR, sample_filename)

filename = 'map_CA.osm'
FILENAME = os.path.join(DIR, filename)


def download(is_sample_run):
    # Download Open Street Map data in XML
    if is_sample_run:
        download_osm_data(url=SAMPLE_URL, filename=SAMPLE_FILENAME)
    else:
        download_osm_data(url=URL, filename=FILENAME)


def parse_xml(is_sample_run):
    """
    This function will parse the XML file into an LXML element tree object
    :param is_sample_run: True/False
    :return: LXML element tree object
    """
    start = time.time()

    print 'Parsing file.\n'
    if is_sample_run:
        print SAMPLE_FILENAME
        doc = le.parse(SAMPLE_FILENAME)
    else:
        print FILENAME
        doc = le.parse(FILENAME)

    print 'Time to read the XML file :: {} seconds'.format(round(time.time() - start, 3))
    return doc


if __name__ == "__main__":
    # Sample Run Status
    sample_run = True

    # Download Map data
    print '------ Downloading OSM XML data -----'
    download(sample_run)

    # Parse XML file
    print '\n------ Parsing OSM XML file ------'
    doc = parse_xml(sample_run)

    # Gather Stats
    print '\n------ XML Document Statistics ------'
    pprint(get_xml_stats(doc))

    print '\n------ Counting keys -------'
    pprint(count_tag_keys(doc))

    # Audit XML document & remove xml elements failed in audit
    print '\n------ Auditing Level 2 Elements -------'
    doc, ids_to_remove = audit_level_2_elements(doc, START_LAT, END_LAT, START_LON, END_LON)

    # Remove node references
    print '\n------ Removing invalid nodes & references ------'
    doc = clear_invalid_node_references(doc, ids_to_remove)

    # Gather Stats
    print '------ XML Document Statistics ------'
    pprint(get_xml_stats(doc))

    # Audit Tag Keys
    print '------ Audit Tag Keys ------'
    pprint(audit_tag_keys(doc))

    # Convert XML elements to JSON docs
    print '------ Create JSON docs from cleaned XML elements ------'
    json_docs = create_json_docs(doc)

    # Creating JSON file
    print '------ Creating JSON file ------'
    if sample_run:
        create_json_file(SAMPLE_FILENAME, json_docs, pretty=True)
    else:
        create_json_file(FILENAME, json_docs, pretty=True)

    # Data import into Mongo DB
    if sample_run:
        fn = SAMPLE_FILENAME
    else:
        fn = FILENAME

    # Start Mongo DB server
    if subprocess.call("mongod &", shell=True) == 0:
        print "... Mongo DB Server Started ..."

    print '------ Importing Data to Mongo DB ------'
    if mongo_data_import(fn):
        print '------ Imported successfully ------'
    else:
        print '------ Data import failed ------'

    client = get_connection()
    db = get_DB(client)
    coll = get_collection(db)

    print '---- Mongo Collection ----'
    print coll

    mongo_data_summary(coll)

    mongo_analyse_data(coll)
