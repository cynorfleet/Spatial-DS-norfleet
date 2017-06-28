import pprint as pp
import os,sys
import json
import collections

DIRPATH = os.path.dirname(os.path.realpath(__file__)) + '\\'

f = open(DIRPATH + "WorldData\\countries.geo.json","r")

data = f.read()

data = json.loads(data)

out = open(DIRPATH +"geo_json\\countries.geojson","w")

out.write(json.dumps(data, sort_keys=False,indent=4, separators=(',', ': ')))
