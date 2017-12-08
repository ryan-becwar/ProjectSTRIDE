import polyline
from ast import literal_eval as make_tuple
import geojson
from geojson import MultiLineString
from geojson import LineString

data = open("part-00000").read()

coords = polyline.decode('ox`vFbpx`SXSTKPSHCTa@Pk@l@g@b@i@\\m@\\Yl@WBIBa@FYDGNGBGDWZs@Jw@Ty@HM')
print(coords)

linestring = LineString(coords)
json = geojson.dumps(linestring)

ofile = open("output.json","w")

ofile.write(json)
ofile.close()
