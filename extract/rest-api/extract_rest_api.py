import requests
import boto3
import json
import configparser
import csv

lat_lng_params = { "lat":42.36,"lon":71.05}

api_response = requests.get( 
    "http://api.open-notify.org/iss-pass.json", 
    params=lat_lng_params)

# Extract the returned results content and loading it to a json file
response_json = json.loads(api_response.content)

all_passes = []

for response in response_json['response']:
    current_pass = []
    # Store the lattitude and longitude from the request
    current_pass.append(lat_lng_params["lat"])
    current_pass.append(lat_lng_params["lon"])

    current_pass.append(response['duration'])
    current_pass.append(response['risetime'])

    all_passes.append(current_pass)

export_file = 'extract_rest_api.csv'

with open(export_file,'w') as fp:
    csvw = csv.writer(fp)
    csvw.writerows(all_passes)

fp.close()