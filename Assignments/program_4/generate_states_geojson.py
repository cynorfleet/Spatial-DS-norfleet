import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__)) + '\\'

all_states = []

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
    for state in data:
        try:
            state_dict = collections.OrderedDict()
            state_dict['type'] = "Feature"
            state_dict['properties'] = state
            state_dict["geometry"] = {}
            state_dict["geometry"]["type"]="Point"
            state_dict["geometry"]["coordinates"] = state.pop('borders')
            all_states.append(state_dict)
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

f = open(DIRPATH + "WorldData\\state_borders.json","r")

data = f.read()

data = json.loads(data)

doDatShit()

out = open(DIRPATH +"geo_json\\states.geojson","w")

out.write(json.dumps(all_states, sort_keys=False,indent=4, separators=(',', ': ')))
