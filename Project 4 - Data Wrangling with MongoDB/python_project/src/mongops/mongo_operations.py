from pymongo import MongoClient
import pymongo, time
import subprocess
import pprint


def mongo_data_import(filename):
    # Import JSON data into MongoDB -- DB Name -- test, collection name -- osm
    start = time.time()
    json_file = '"{0}".json'.format(filename)
    import_cmd = "mongoimport --db test --collection osm --drop --file {}".format(json_file)

    print "Running below cmd to load json file data into mongodb(test -> osm) \n {}".format(import_cmd)

    if subprocess.call(import_cmd, shell=True) == 0:
        print "... Import Successful ..."
        print 'Time Taken :: ', round(time.time() - start, 3), " seconds"
        return True
    else:
        return False


def get_connection():
    return MongoClient()


def get_DB(client):
    return client.test


def get_collection(db):
    return db.osm


def mongo_data_summary(coll):
    # Total documents
    total_docs = coll.count()
    print "Total documents in MongoDB OSM collection :: ", total_docs

    # Find One document
    print "----- First Document ----"
    pprint.pprint(coll.find_one())

    print "----- Total documents by user -- {} -----".format("86782")
    coll.find({"created.uid": "86782"}).count()

    print "----- One document by user -- {} -----".format("86782")
    pprint.pprint(coll.find_one({"created.uid":"86782"}))

    print "----- Total Documents with postcode -- {} -----".format("90278")
    coll.find({"address.postcode": "90278"}).count()

    for doc in coll.find({"address.postcode": "90278"}):
        pprint.pprint(doc)


def mongo_analyse_data(coll):
    total_docs = coll.count()

    # Find out all distinct tag types
    print "Distinct types :: "
    coll.distinct("type")

    # Find document types with respective count
    print "Document counts by types :: "
    pipeline = [
        {
            "$sortByCount": "$type"
        }
      ]
    cursor = coll.aggregate(pipeline)
    for doc in cursor:
        pprint.pprint(doc)

    print "Top 10 contributors :: "
    pipeline = [
        {
            "$sortByCount": "$created.user"
        },
        {
            "$limit":10
        },
        {
            "$project": {
                "_id" : 1,
                "count": 1,
                "percent": { "$divide": ["$count", total_docs/100.0] }
            }
        }
      ]

    cursor = coll.aggregate(pipeline)
    for doc in cursor:
        doc['percent'] = round(doc['percent'], 2)
        pprint.pprint(doc)

    # Do the same using map reduce in Mongo
    print "Top 10 contributors(using Mongo DB Map-Reduce) :: "
    map_function = "function () { emit(this.created.user, 1); }"
    reduce_function = "function (key, value) { return Array.sum(value); }"

    # Results will be saved in a different collection
    mr_coll = coll.map_reduce(map_function, reduce_function, "osm_map_reduce_example")

    pipeline = [
        {"$project": {"_id":1, "count": "$value"} },
        {"$sort": {"count":-1} },
        {"$limit": 10}
    ]

    cursor = mr_coll.aggregate(pipeline)
    for doc in cursor:
        print doc

    print "Top Amenity types :: "
    field = "amenity"
    pipeline = [
        {"$group": {"_id": "$"+field, "count": {"$sum": 1} } },
        {"$match": {"_id": {"$ne": None } } },
        {"$sort": {"count":-1} }
    ]

    cursor = coll.aggregate(pipeline)
    for document in cursor:
        print(document)

    print "Top Cuisine types :: "
    field = "cuisine"
    pipeline = [
        {"$group": {"_id": "$"+field, "count": {"$sum": 1} } },
        {"$match": {"_id": {"$ne": None } } },
        {"$sort": {"count":-1} }
    ]
    cursor = coll.aggregate(pipeline)

    for document in cursor:
        print(document)

    print "Top places for worship:: "
    pipeline = [
        {
            "$match": {"amenity" :"place_of_worship"}
        },
        {
            "$project": {"_id":0, "name": 1}
        }
    ]

    cursor = coll.aggregate(pipeline)
    for doc in cursor:
        pprint.pprint(doc["name"])

    print "Top places to eat or drink:: "
    pipeline = [
        {
            "$match": {"amenity" : {"$in": ["fast_food", "cafe", "pub", "bar"] } }
        },
        {
            "$project": {"_id":1, "name": 1}
        }
    ]

    cursor = coll.aggregate(pipeline)
    for doc in cursor:
        pprint.pprint(doc)

    print "Find cinema halls :: "
    pipeline = [
        {
            "$match": {"amenity" :  {"$in": ["cinema", "theatre"]} }
        },
        {
            "$project": {"_id":1, "name": 1}
        }
    ]

    cursor = coll.aggregate(pipeline)
    for doc in cursor:
        pprint.pprint(doc)

    print "Find all street names :: "
    field = "address.street"
    pipeline = [
        {"$group": {"_id": "$"+field, "count": {"$sum": 1} } },
        {"$match": {"_id": {"$ne": None } } },
        {"$sort": {"count":-1} }
    ]
    cursor = coll.aggregate(pipeline)

    for document in cursor:
        print(document)

    print "Find all postcodes with count:: "
    field = "address.postcode"
    pipeline = [
        {"$group": {"_id": "$"+field, "count": {"$sum": 1} } },
        {"$match": {"_id": {"$ne": None } } },
        {"$sort": {"count":-1} }
    ]
    cursor = coll.aggregate(pipeline)

    for document in cursor:
        print(document)

    print "Top change Sets:: "
    pipeline = [
        {
            "$sortByCount": "$created.changeset"
        },
        {
            "$limit":10
        },
        {
            "$project": {
                "_id" : 1,
                "count": 1,
                "pct": { "$divide": ["$count", total_docs/100.0] }
            }
        }
      ]
    cursor = coll.aggregate(pipeline)
    for doc in cursor:
        doc['pct'] = round(doc['pct'], 2)
    pprint.pprint(doc)

    print "Create a text serach index and get tge index info"
    ### Create index on name field
    coll.create_index([
            ("name", pymongo.TEXT)
        ])

    ### Index information
    pprint.pprint(coll.index_information())

    ### Search using the text index on name for school
    print "Search for school using the TEXT index:: "
    cursor = coll.find( { "$text": { "$search": "school" } },
                        { "_id":0, "name":1, "amenity":1, "type":1 }
                      )

    for doc in cursor:
        pprint.pprint(doc)

    print "Extract Day, Month, Year from create timestamp:: "
    cursor = coll.aggregate([
            {"$project" : {
                "_id": 1, "type": 1, "pos": 1, "name": 1,
                "year": { "$year": "$created.timestamp" },
                "month": { "$month": "$created.timestamp" },
                "day": { "$dayOfMonth": "$created.timestamp" }
                }
            }
        ])

    for doc in cursor:
        pprint.pprint(doc)
        break

    print "Find years of modification with respective counts:: "
    pipeline = [
        {
            "$project": {"year": { "$year": "$created.timestamp" }}
        },
        {
            "$sortByCount": "$year"
        }
      ]
    cursor = coll.aggregate(pipeline)
    for doc in cursor:
        pprint.pprint(doc)

    print "Do Explain plan like Oracle -- Query Execution Plan :: "
    pipeline = [
        {
            "$project": {"year": { "$year": "$created.timestamp" }}
        },
        {
            "$sortByCount": "$year"
        }
      ]

    for doc in coll.find( { "$query": {}, "$explain": 1 } ):
        pprint.pprint(doc)

    print "A lot of empty data were present in the dataset. Only node info, not much other info."
    print "percent of non-empty elements"

    cursor = coll.find( {"$or": [{"address": {"$exists": 1}},
                                 {"name": {"$exists": 1}},
                                 {"amenity": {"$exists": 1}},
                                 {"cuisine": {"$exists": 1}},
                                 {"node_refs": {"$exists": 1}}
                                ]}
                       )
    count = cursor.count()
    print 'Total Tags :: ', total_docs
    print 'Non Empty data tags :: ', count
    print 'Percent of XML element having meaningful data :: {}%'.format(round(count * 100.0/ total_docs, 2))
