import polyline
from ast import literal_eval as make_tuple
import geojson
from geojson import MultiLineString

_, data = open("part-00000").read().strip().split('\t')

segments, score = make_tuple(data)

segcoords = []
for seg in segments:
    line = polyline.decode(seg[2])
    segcoords.append(line)

#geojson format wants coords to be swapped
segcoords = [[(c[1], c[0]) for c in seg] for seg in segcoords]

linestring = MultiLineString(segcoords)
json = geojson.dumps(linestring)

ofile = open("output.json","w")

ofile.write(json)
ofile.close()
