# EXAMPLE API CALL WITHOUT AUTHENTICATION

import requests
import json

def jprint(obj):

   text = json.dumps(obj, sort_keys=True, indent=4)
   print(text)

response = requests.get("http://api.open-notify.org/astros.json")

print(response.status_code)
200

jprint (response.json())
{
    "message": "success",
    "number": 3,
    "people": [
        {
            "craft": "ISS",
            "name": "Chris Cassidy"
        },
        {
            "craft": "ISS",
            "name": "Anatoly Ivanishin"
        },
        {
            "craft": "ISS",
            "name": "Ivan Vagner"
        }
    ]
}

print (response.json()["message"])
success

print (response.json()["people"][0]["name"])
print (response.json()["people"][1]["name"])
Chris Cassidy
Anatoly Ivanishin

#  API CALL WITH PARAMETERS PASSING
parameters = {
    "lat": 40.71,
    "lon": -74
}

response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
print (response.status_code)
jprint(response.json())

200
{
    "message": "success",
    "request": {
        "altitude": 100,
        "datetime": 1587086081,
        "latitude": 40.71,
        "longitude": -74.0,
        "passes": 5
    },
    "response": [
        {
            "duration": 301,
            "risetime": 1587121298
        },
        {
            "duration": 638,
            "risetime": 1587126890
        },
        {
            "duration": 588,
            "risetime": 1587144459
        }
    ]
}

#  EXTRACT ONLY THE response ELEMENT

pass_times = response.json()['response']
jprint(pass_times)

[
    {
        "duration": 301,
        "risetime": 1587121298
    },
    {
        "duration": 638,
        "risetime": 1587126890
    },
    {
        "duration": 588,
        "risetime": 1587144459
    }
]

#  EXTRACT ONLY THE risetimes ELEMENTS
risetimes = []

for d in pass_times:
    time = d['risetime']
    risetimes.append(time)

print(risetimes)

[1587121298, 1587126890, 1587144459]

#  PRINT THE risetimes IN READABLE FORMAT
from datetime import datetime

times = []

for rt in risetimes:
    time = datetime.fromtimestamp(rt)
    times.append(time)
    print(time)

2020-04-17 04:01:38
2020-04-17 05:34:50
2020-04-17 10:27:39

#   TEST THE RETURN CODE
response = requests.get('https://google.com/api')
print (response)
if response:
   print ('Request is successful.')
else:
   print ("Request returned an error.")

#  API CALL WITH AUTHORIZATION CODE REQUIRED (using headers)
import requests

res = requests.post('https://api.short.cm/links', {
      'domain': 'run.resourceonline.org',
      'originalURL': 'https://oval.stanford.edu/roles.html',
}, headers = {
      'authorization': 'some-auth-string'
}, json=True)

res.raise_for_status()
data = res.json()

#   API CALL WITH AUTHORIZATION CODE AND PAYLOAD
import requests

url = "https://api.short.cm/domains/"

payload = "{\"hostname\":\"digital.resourceonline.org\",\"rootredirect\":\"http://uit.stanford.edu\",\"linkType\":\"random\"}"
headers = {
    'accept': "application/json",
    'authorization': 'xxxxxxxxauth-codexxxxxxxx',
    'content-type': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)

#   end of the lesson
