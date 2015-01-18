import shutil
import requests
import json
import os, sys, time

tmp_directory = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + "/../tmp") + '/'

file_types = {
	'.kml' : '.kml',
	'.geojson' : '.geojson',
	'/geometry' : '.json',
}


# Request parameters
mapit_domain = "http://mapit.mysociety.org"
mapit_headers = {'User-Agent': 'Mike Thompson | Constituency Map'}
mapit_path  = "/areas/WMC"
url = mapit_domain + mapit_path

# Fetch JSON for all Parliamentary constituencies
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
geometry_extension = "/geometry" # Change to e.g. .kml, .geojson for other file types

# Loop through areas and save KML files
for area_id, area_data in data.iteritems():

	url = mapit_domain + mapit_path + area_id + geometry_extension
	outfile = tmp_directory + area_id + file_types[geometry_extension]

	print url + ", " + area_data["name"]

	# Avoid rate limiting
	time.sleep(1.3)
	
	# Request file
	try:
		response = requests.get(url, headers = mapit_headers, stream = True)
	except:
		time.sleep(5)
		response = requests.get(url, headers = mapit_headers, stream = True)

	# Debug and exit if request failed
	if( response.status_code != requests.codes.ok ):
		print 'Request failed for ' + area_id + ': ' + str(response.status_code) + ', ' + response.text
	else:
		with open(outfile, 'wb') as f:
			response.raw.decode_content = True
			shutil.copyfileobj(response.raw, f)

	del response