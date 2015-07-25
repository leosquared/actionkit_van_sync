import requests, json, pprint
from requests.auth import HTTPBasicAuth
from VAN_CREDENTIALS import api_user, api_key

find_or_create = 'https://api.securevan.com/v4/people/findOrCreate'
find = 'https://api.securevan.com/v4/people/101409539'
event = 'https://api.securevan.com/v4/events/11063'
event_types = 'https://api.securevan.com/v4/events/types'


test_vanid = '102606750'
test_event_id = '11063'

test_person = {
	'firstName':'Leo',
	'lastName':'Chiang',
	'phone':{
		'phoneNumber':'17189150686',
		'phoneType':'M'
		},

	'email':{
		'email':'lchiang@maig.org'
		},

	'address':{
		'addressLine1':'123 Main Street',
		'city':'New York',
		'stateOrProvince':'NY',
		'zipOrPostalCode':'11101',
		'countryCode':'US',
		'type':'H'
	}

}

headers = {'Content-type':'application/json'}

params = {
	'$expand':'phones,emails,addresses'
}

# r = requests.post(find_or_create, data=json.dumps(test_person), headers=headers, auth=(api_user, api_key)) # create person

event_params = {
	'startingAfter':'2015-07-22',
	'$expand':'locations,codes,shifts,roles'
}

# r = requests.get(event, params=event_params, auth=(api_user, api_key)) # get event info

person_params = {
	'$expand':'phones,emails,addresses'
}

r = requests.get(find, params=person_params, auth=(api_user, api_key)) # find Leo Chiang

print r
pprint.pprint(r.json())

