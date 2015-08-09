import requests, json, pprint, csv, datetime
from StringIO import StringIO
from collections import OrderedDict
from VAN_CREDENTIALS import api_user, api_key
from AK_CREDENTIALS import ak_user, ak_pw


def get_ak_report(report_short_name):

	""" ping ActionKit's report API to run the report, limited to 1,000 rows only """

	report_url = 'https://donate.everytown.org/rest/v1/report/run/{0}/'.format(report_short_name)
	params = {
		'format':'tsv'
	}

	r = requests.post(report_url, params=params, auth=(ak_user, ak_pw))
	
	result_file = StringIO(r.text)

	return csv.reader(result_file, delimiter='\t')


def event_details(person_object):

	""" get location id, role id, shift id, status id using /events/ endpoint """

	url = 'https://api.securevan.com/v4/events/'
	details_params = {
		'$expand':'locations,shifts,roles'
	}

	if person_object.get('van_event_id'):
		event_id = person_object['van_event_id']
		r = requests.get(url + str(event_id), params=details_params, auth=(api_user, api_key)) 
		details = r.json()

		person_object['location_id'] = details.get('locations')[0]['locationId']
		person_object['role_id'] = details.get('roles')[0]['roleId']
		person_object['shift_id'] = details.get('shifts')[0]['eventShiftId']
		person_object['status_id'] = 1

	return person_object


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

	# if person_object.get('akid'):
	# 	person['identifiers'] = [
	# 		{
	# 		'type':'AKID',
	# 		'externalId':person_object.get('akid')
	# 		}
	# 	]

	url = 'https://api.securevan.com/v4/people/findOrCreate'
	headers = {'Content-type':'application/json'}
	r = requests.post(url, data=json.dumps(person), headers=headers, auth=(api_user, api_key)) # create person

	person_object['vanid'] = r.json().get('vanId')

	return person_object


def event_signup(person_object):

	""" function to sign up people individually to events specified in the person_object """

	signup = {
		"person": {
		"vanId": person_object.get('vanid'),
		},
		"event": {
		"eventId": person_object.get('van_event_id'),
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

	person_object['signup_id'] = r.text

	return person_object


""" Load lookup dictionary of ak event id to van event id """

lu_file = csv.reader(open('lu_van_ak_events.csv'))
lu_file.next()
lu_van_ak = {}
for row in lu_file:
	lu_van_ak[row[1]] = row[0]


""" Load file """

infile = get_ak_report('reporting-daily-events-upload-2')
headers = infile.next()


""" Begin iterating """

data = OrderedDict([])
for index, row in enumerate(infile):
	person = OrderedDict([])
	for col, header in enumerate(headers):
		person[header] = row[col]

		if header == 'ak_event_id':
			person['van_event_id'] = lu_van_ak.get(row[col])


	person = event_details(person)
	person = find_or_create(person)
	person = event_signup(person)

	data[index] = person


""" Write Results to file """

time_now = datetime.datetime.now().strftime('%m.%d.%y-%H.%M')
outfile = csv.writer(open(time_now + '_result.csv', 'w'))
headers = data[0].keys()
outfile.writerow(headers)

for row in data:
	outfile.writerow(data[row].values())
