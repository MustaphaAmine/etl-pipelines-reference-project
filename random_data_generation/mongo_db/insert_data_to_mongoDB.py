from pymongo import MongoClient
import datetime
import configparser
import json
import certifi

# load mongo configuration values
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("mongo_config","hostname")
username = parser.get("mongo_config","username")
password = parser.get("mongo_config","password")
database_name = parser.get("mongo_config","database")
collection_name = parser.get("mongo_config","collection")

# Here I am using MongoDB Atlas, you generate the connection link to connect to your cluster using their dashboard
mongoClient = MongoClient("mongodb://root:" + password 
                        + "@testingcluster-shard-00-00.9wce0.mongodb.net:27017," 
                        + "testingcluster-shard-00-01.9wce0.mongodb.net:27017,"
                        + "testingcluster-shard-00-02.9wce0.mongodb.net:27017/" 
                        + database_name + "?ssl=true&replicaSet=atlas-6ii87s-shard-0&authSource=admin&retryWrites=true&w=majority"
                        ,tlsCAFile=certifi.where())

mongo_db = mongoClient[database_name]
mongo_collection = mongo_db[collection_name]

# loading posts data from a json file 
with open("random_data_generation/mongo_db/posts.json" ,'r') as fp: 
    posts_list = json.load(fp)

# loading posts data from a json file posts
with open("random_data_generation/mongo_db/authors.json" ,'r') as fp: 
    authors_list = json.load(fp)

mongo_collection.insert_many(posts_list)
mongo_collection.insert_many(authors_list)
