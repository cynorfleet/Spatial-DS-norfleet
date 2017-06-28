import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__)) + '\\'

all_volcanoes = []

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
    for volcanoe in data:
        try:
            volcanoes_dict = collections.OrderedDict()
            volcanoes_dict['type'] = "Feature"
            volcanoes_dict['properties'] = volcanoe
            lat = (float)(volcanoe['Lat'])
            lon = (float)(volcanoe['Lon'])
            del volcanoes_dict['properties']['Lat']
            del volcanoes_dict['properties']['Lon']
            volcanoes_dict["geometry"] = {}
            volcanoes_dict["geometry"]["type"]="Point"
            volcanoes_dict["geometry"]["coordinates"] = [
                lon,
                lat
                ]
            all_volcanoes.append(volcanoes_dict)
            counter +=1
            # Break if reached 1000 items
            if counter == limit:
                print("Limit Reached: %d" % counter)
                return
            if counter >= limit:
                print("Uhh OHHHHHHH")
                break
        except Exception as e:
            print("SKIPPING ENTRY %s" % str(e))


#pp.pprint(all_airports)

f = open(DIRPATH + "WorldData\\world_volcanos.json","r")

data = f.read()

data = json.loads(data)

doDatShit()

out = open(DIRPATH +"geo_json\\volcanoes.geojson","w")

out.write(json.dumps(all_volcanoes, sort_keys=False,indent=4, separators=(',', ': ')))
