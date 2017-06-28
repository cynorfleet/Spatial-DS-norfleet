import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__)) + '\\'

all_cities = []

'''
      "geometry": {
        "type": "Point",
        "coordinates": [
          -120.966003418,
          42.3642997742
        ]
      }
'''

def doDatShit(limit=1000):
    counter = 1;
    for k,v in data.items():
        citiesdict = collections.OrderedDict()
        for city in v: 
            citiesdict['type'] = "Feature"
            citiesdict['properties'] = city
            lat = (float)(city['lat'])
            lon = (float)(city['lon'])
            del citiesdict['properties']['lat']
            del citiesdict['properties']['lon']
            citiesdict["geometry"] = {}
            citiesdict["geometry"]["type"]="Point"
            citiesdict["geometry"]["coordinates"] = [
                lon,
                lat
                ]
            all_cities.append(citiesdict)
            counter +=1
            # Break if reached 1000 items
            if counter == limit:
                print("Limit Reached: %d" % counter)
                return
            if counter >= limit:
                print("Uhh OHHHHHHH")
                break


#pp.pprint(all_airports)

f = open(DIRPATH + "WorldData\\world_cities_large.json","r")

data = f.read()

data = json.loads(data)

doDatShit()

out = open(DIRPATH +"geo_json\\cities.geojson","w")

out.write(json.dumps(all_cities, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()