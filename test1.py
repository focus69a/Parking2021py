import requests
import json
#import sys #pozwala drukowac na konsole komunikaty i tylko po to
#import dns # to jest po to żeby zadziałał protokół łączenia do mongo w AWS 

RESTlink = 'https://nominatim.openstreetmap.org/?addressdetails=1&q='
RESTquery = 'Urząd+Skarbowy+Warszawa'
RESTparm = '&format=json&limit=5'
query = RESTlink + RESTquery + RESTparm
response = requests.get(query)
print(response.json())

struktura = response.json()

print(struktura[0]["lat"] + " " + struktura[0]["lon"] )
print(struktura[1]["lat"] + " " + struktura[1]["lon"] )
print(struktura[2]["lat"] + " " + struktura[2]["lon"] )

parsed = json.loads(response.text)
print(json.dumps(parsed, indent=4, sort_keys=True))

print(len(struktura))