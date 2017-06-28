import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__)) + '\\'

all_quakes = []

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
        quakedict = collections.OrderedDict()
        for quake in v: 
            quakedict['type'] = "Feature"
            quakedict['properties'] = quake
            lat = quake['geometry']['coordinates'][0]
            lon = quake['geometry']['coordinates'][1]
            del quakedict['properties']['geometry']
            quakedict["geometry"] = {}
            quakedict["geometry"]["type"]="Point"
            quakedict["geometry"]["coordinates"] = [
                lon,
                lat
                ]
            all_quakes.append(quakedict)
            counter +=1
            # Break if reached 1000 items
            if counter == limit:
                print("Limit Reached" + counter)
                return
            if counter >= limit:
                print("Uhh OHHHHHHH")
                break


#pp.pprint(all_airports)

f = open(DIRPATH + "WorldData\\earthquakes-1960-2017.json","r")

data = f.read()

data = json.loads(data)

doDatShit()

out = open(DIRPATH +"geo_json\\earthquakes.geojson","w")

out.write(json.dumps(all_quakes, sort_keys=False,indent=4, separators=(',', ': ')))

out.close()