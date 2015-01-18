#
# This script is used to create a single GeoJSON file of Features 
# representing the centroids of UK parliamentary constituencies
# constituencies with no polygon data are recorded in no_data and 
# printed at the end.
#

import shutil
import requests
import json
import os, sys, time

# Where to save the output
data_directory = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "/../data") + '/'
output_file = data_directory + "uk-constituency-centroids.json"

# Create list to contain GeoJSON feature definition for each constituency
features = []

# Create list to record which areas have no polygon data
no_data = []

# Request parameters
mapit_domain = "http://mapit.mysociety.org"
mapit_headers = {'User-Agent': 'Mike Thompson | Constituency Map'}
mapit_path  = "/areas/WMC"
url = mapit_domain + mapit_path

# Fetch MapIt JSON for all Parliamentary constituencies
try:
	response = requests.get(url, headers = mapit_headers)
except:
	time.sleep(5)
	response = requests.get(url, headers = mapit_headers)

# Debug and exit if request failed
if( response.status_code != requests.codes.ok ):
	print 'Request failed: ' + str(response.status_code) + ', ' + response.text
	sys.exit()

# Load response into JSON object
data = json.loads(response.text)

# Different request parameters
mapit_path  = "/area/"
geometry_extension = "/geometry"

# Loop through areas and save geometry files
for area_id, area_data in data.iteritems():
	
	url = mapit_domain + mapit_path + area_id + geometry_extension

	print url + ", " + area_data["name"]

	# Play nice with rate limiting
	time.sleep(0.5)
	
	# Request file
	try:
		response = requests.get(url, headers = mapit_headers, stream = True)
	except:
		time.sleep(5)
		response = requests.get(url, headers = mapit_headers, stream = True)

	# Debug and exit if request failed
	if( response.status_code != requests.codes.ok ):
		print 'Request failed for ' + area_id + ': ' + str(response.status_code) + ', ' + response.text
		no_data.append((area_id, area_data['name']))
		area_coordinates = None
	else:
		# Load response into JSON object
		data = json.loads(response.text)
		area_coordinates = [data["centre_lon"], data["centre_lat"]]

	area_feature = { 
		"type" : "Feature",
		"id" : area_data['codes']['gss'],
		"geometry" : { 
			"type" : "Point",
			"coordinates" : area_coordinates
		 },
		"properties" : {
			"name" : area_data['name'],
			"mapit_id" : area_id,
		}
	}

	features.append(area_feature)

output = {	
	"type" : "FeatureCollection",
	"features": features 
}

with open(output_file, 'wb') as f:
    json.dump(output, f, indent=3)

print no_data