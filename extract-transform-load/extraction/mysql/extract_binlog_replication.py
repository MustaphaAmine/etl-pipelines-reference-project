from pymysqlreplication import BinLogStreamReader
from pymysqlreplication import row_event
import configparser
import pymysqlreplication
import csv

# get the MySQL connection info
parser = configparser.ConfigParser()
parser.read("pipeline.conf") 
hostname = parser.get("mysql_config", "hostname") 
port = parser.get("mysql_config", "port") 
username = parser.get("mysql_config", "username") 
password = parser.get("mysql_config", "password")

mysql_settings = { 
    "host": hostname,
    "port": int(port), 
    "user": username, 
    "passwd": password }

b_stream = BinLogStreamReader(
    connection_settings = mysql_settings,
    server_id = 100,
    only_events = [ row_event.DeleteRowsEvent,
                    row_event.WriteRowsEvent,
                    row_event.UpdateRowsEvent]
)
posts_events = list()


for binlogEvent in b_stream:
    for row in binlogEvent.rows:
        if binlogEvent.table == "posts":
            event = dict()
            if isinstance(binlogEvent, row_event.DeleteRowsEvent):
                event["action"] = "delete"
                event.update(row["values"].items())
            elif isinstance(binlogEvent, row_event.UpdateRowsEvent):
                event["action"] = "update"
                event.update(row["after_values"].items())
            elif isinstance(binlogEvent, row_event.WriteRowsEvent):
                event["action"] = "insert"
                event.update(row["values"].items())
            posts_events.append(event)

b_stream.close()

keys = posts_events[0].keys()
local_filename = 'post_extracts.csv'
with open(
        local_filename,
        'w',
        newline='') as output_file:
    dict_writer = csv.DictWriter(
        output_file,
        keys)
    dict_writer.writerows(posts_events)

# uploading the data to boto3_aws