import requests
import sys
import os


def download_osm_data(url, filename, timeout=30):
    """
    This function will request the Overpass API URL to get map data
    according to the Lat & Lon boundaries provided.
    It also accepts an optional parameter as timeout to wait for
    specified time until timeout.
    The data will be written to the output file mentioned.
    :param url: http://overpass-api.de/api/map?bbox={START_LON},{START_LAT},{END_LON},{END_LAT}
    :param filename: Name of the file to save
    :param timeout: Timeout in seconds for the operation, default is 30 seconds
    """
    print "Requesting URL :: ", url
    r = requests.get(url, stream=True, timeout=30)

    if r.status_code == 200:
        print 'Request successful !!!'
        with open(filename, 'wb') as f:
            print "Downloading data to file."
            i = 0
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    i += 1
                    f.write(chunk)
                    if i % 3 == 0:
                        sys.stdout.write("\r%s" % ('.'*(i/5)))
                        sys.stdout.flush()

        print '\nDownload finished. \n{} is ready.'.format(filename)
        print 'File Size :: {} MB'.format(round(os.path.getsize(filename) / (1024.0 * 1024), 3))
    else:
        print "Bad Request...\n\n", r.content
