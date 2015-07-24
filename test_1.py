import requests, json, pprint, csv, sys
from collections import OrderedDict
from VAN_CREDENTIALS import api_user, api_key


def find_or_create(person_object):
	
	""" Write function to find or create person """

	person = {
		'firstName':person_object.get('first_name'),
		'middleName':person_object.get('middle_name'),
		'lastName':person_object.get('last_name')
		}

	if person_object.get('phone'):
		person['phone'] = {
			'phoneNumber':person_object.get('phone')
			}

	if person_object.get('email'):
		person['email'] = {
			'email':person_object.get('email')
			}

	if person_object.get('zipcode') or person_object.get('state'):
		person['address'] = {
			'addressLine1':person_object.get('address1'),
			'city':person_object.get('city'),
			'stateOrProvince':person_object.get('state'),
			'zipOrPostalCode':person_object.get('zipcode'),
			'countryCode':'US',
			'type':'H'
			}


	url = 'https://api.securevan.com/v4/people/findOrCreate'
	headers = {'Content-type':'application/json'}
	r = requests.post(url, data=json.dumps(person), headers=headers, auth=(api_user, api_key)) # create person

	return r.json().get('vanId')


def event_signup(person_object):

	""" function to sign up people individually to events specified in the person_object """

	signup = {
		"person": {
		"vanId": person_object.get('vanid'),
		},
		"event": {
		"eventId": person_object.get('event_id'),
		},
		"shift": {
		"eventShiftId": person_object.get('shift_id'),
		},
		"role": {
		"roleId": person_object.get('role_id')
		},
		"status": {
		"statusId": person_object.get('status_id')
		},
		"location": {
		"locationId": person_object.get('location_id')
		}
	}


	url = 'https://api.securevan.com/v4/signups'
	headers = {'Content-type':'application/json'}
	r = requests.post(url, data=json.dumps(signup), headers=headers, auth=(api_user, api_key)) # signup or update a signup to an event

	return r.json()





infile = csv.reader(open(sys.argv[1], 'rU'))

headers = infile.next()
data = OrderedDict([])

for index, row in enumerate(infile):
	data[index] = OrderedDict([])
	for col, header in enumerate(headers):
		data[index][header] = row[col]

	vanid = find_or_create(data[index])
	data[index]['vanid'] = vanid

	print event_signup(data[index])


print data

""" put person in one by one using findOrCreate """
""" save resulting VANIDs to dictionary """