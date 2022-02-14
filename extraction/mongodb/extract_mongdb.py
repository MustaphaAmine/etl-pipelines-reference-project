from pymongo import MongoClient 
import csv 
import boto3 
import datetime 
from datetime import timedelta 
import configparser
import certifi

# load mongo configuration values
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("mongo_config","hostname")
username = parser.get("mongo_config","username")
password = parser.get("mongo_config","password")
database_name = parser.get("mongo_config","database")
collection_name = parser.get("mongo_config","collection")

# Here I am using MongoDB Atlas, you can generate the connection link to connect to your cluster from their dashboard
mongoClient = MongoClient("mongodb://root:" + password 
                        + "@testingcluster-shard-00-00.9wce0.mongodb.net:27017," 
                        + "testingcluster-shard-00-01.9wce0.mongodb.net:27017,"
                        + "testingcluster-shard-00-02.9wce0.mongodb.net:27017/" 
                        + database_name + "?ssl=true&replicaSet=atlas-6ii87s-shard-0&authSource=admin&retryWrites=true&w=majority"
                        ,tlsCAFile=certifi.where())

mongo_db = mongoClient[database_name]
mongo_collection = mongo_db[collection_name]

# this is a simple query that tells mongodb to extract only the authors added after the 4th of mai 2006
mongo_query = { "added" : {"$gte" : str(datetime.datetime(2006, 5, 4))}}
authors_docs = mongo_collection.find(mongo_query, batch_size=30)

# create a blank list to store the authors
all_authors = list()

for author in authors_docs:
    # adding default values
    _id = str(author.get("id", -1))
    first_name = author.get("first_name",None)
    last_name = author.get("last_name",None)
    email = author.get("email",None)
    birthdate = author.get("birthdate",None)
    insertion_datetime = author.get("added",None)

    # adding the author to the list of authors
    all_authors.append([_id,first_name,last_name,email,birthdate,insertion_datetime])

export_file = "export_authors.csv"

with open(export_file, 'w') as fp: 
    csvw = csv.writer(fp) 
    csvw.writerows(all_authors)

fp.close()