import requests
import json
import os

#the initial code we had written calls the API url for each bikepoint, we want to get all 

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

        file_list = [f for f in os.listdir('.') if f.endswith('.json')]

        filename = modified+bp+'.json'
        if filename in file_list:
            print('Up to date')
        else:
            with open(filename, 'w') as file:
                json.dump(bike_point, file)
else:
    #this bit gets a cleaner error message
    data = response.json()
    error_message = data.get("message","No message provided.")
    print(f'Error {response.status_code}: {error_message}')