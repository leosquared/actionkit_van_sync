import requests, json, pprint
from requests.auth import HTTPBasicAuth

find_or_create = 'https://api.securevan.com/v4/people/findOrCreate'
find = 'https://api.securevan.com/v4/people/'

vanid = '100501330'

api_user = 'MAIG.APIUser'
api_key = '8B298C14-393F-49D0-B471-D9520830B89B|1'

test_person_id = '102606750'
test_event_id = '11063'

data = {
	'firstName':'Leo',
	'middleName':'Matthew',
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

# data = {
#   "firstName": "James",
#   "middleName": "Worthington",
#   "lastName": "Gordon",
#   "email": {
#     "email": "jim@gotham.city.us",
#     "isPreferred": True
#   },
#   "phone": {
#     "phoneNumber": "1-555-555-1234",
#     "phoneType": "W",
#     "ext": 999,
#     "isPreferred": True
#   },
#   "address": {
#     "addressLine1": "123 Main St",
#     "addressLine2": "Apt 3",
#     "addressLine3": "Blah",
#     "city": "Gotham City",
#     "stateOrProvince": "IL",
#     "zipOrPostalCode": "01234",
#     "countryCode": "US",
#     "type": "H",
#     "isPreferred": False
#   }
# }

headers = {'Content-type':'application/json'}

params = {
	'$expand':'phones,emails,addresses'
}

# r = requests.post(find_or_create, data=json.dumps(data), headers=headers, auth=(api_user, api_key)) # create
r = requests.get(find + test_person_id, params=params, auth=(api_user, api_key)) # find
print r
pprint.pprint(r.json())
