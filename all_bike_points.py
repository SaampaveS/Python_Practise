import requests
import json
import os
import boto3
import os
from dotenv import load_dotenv
from load_test import load_to_s3

#the initial code we had written calls the API url for each bikepoint, we want to get all 

load_dotenv()

access_key = os.getenv('AWS_ACCESS_KEY')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key
)

url = 'https://api.tfl.gov.uk/BikePoint'
response = requests.get(url)

if response.status_code== 200:

    data=response.json()

    number_of_bike_points = len( [item.get('id') for item in data])

    for i in range(0, number_of_bike_points-1):
        bike_point = data[i]

        #get modified timestamp to help us build our file. The [0] outputs tehe first modified number
        first_value = bike_point['additionalProperties'][0]
        modified = first_value.get('modified')
        modified = modified.replace(':','-')
        modified = modified.replace('.','-')
        
        bp = bike_point.get('id')

        filename = modified+bp+'.json'

        s3_contents = s3_client.list_objects_v2(Bucket=bucket)
        file_list = [item['Key'] for item in s3_contents.get('Contents', [])]

        if filename in file_list:
            print('Up to date')
        else:
            with open(filename, 'w') as file:
                json.dump(bike_point, file)
            load_to_s3(filename)
            print('Uploaded '+ filename)
else:
    #this bit gets a cleaner error message
    data = response.json()
    error_message = data.get("message","No message provided.")
    print(f'Error {response.status_code}: {error_message}')