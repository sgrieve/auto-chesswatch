import os
import sys
import json
import requests
from collections import OrderedDict
from datetime import datetime, timedelta

measurement_id = sys.argv[1]
station_id = measurement_id.split('-')[0]
base_path = sys.argv[2]

json_path = os.path.join(base_path, '{}.json'.format(measurement_id))
csv_path = os.path.join(base_path, '{}.csv'.format(measurement_id))

with open(json_path) as f:
    measurements = json.load(f)

root = 'http://environment.data.gov.uk/flood-monitoring'

# Find the most recent measurement we have stored in the csv
with open(csv_path) as f:
    most_recent = f.readlines()[-1].split(',')[0]

# Call the API to get the new data
r = requests.get('{}/id/stations/{}/readings?_sorted&since={}Z'.format(root, station_id, most_recent))
response = r.json()
data = response['items']

modified = False

# Update our dict
for d in data:
    if d['measure'].endswith(measurement_id):
        measurements[d['dateTime'][:-1]] = d['value']
        modified = True


# Sort the updated json by date and write it to csv
sorted_dict = OrderedDict(sorted(measurements.items()))
with open(csv_path, 'w') as w:
    w.write('date,measurement\n')
    for date, measurement in sorted_dict.items():
        w.write('{},{}\n'.format(date, measurement))

if modified:
    # Back up yesterday's data, overwriting previous backup
    os.replace(json_path, '{}.bak'.format(json_path))

    # Write the new, updated dict to json
    with open(json_path, 'w') as f:
         f.write(json.dumps(measurements))
