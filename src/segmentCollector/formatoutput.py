import polyline
from ast import literal_eval as make_tuple
import geojson
from geojson import MultiLineString, Feature, FeatureCollection

_, data = open("part-00000").read().strip().split('\t')

segments, score = make_tuple(data)

segcoords = []
for seg in segments:
    line = polyline.decode(seg[2])
    segcoords.append(line)

connectors = []
for i in range(len(segments)):
    connection = []
    connection.append(segments[i][1])
    connection.append(segments[(i+1)%len(segments)][0])
    connectors.append(connection)


#geojson format wants coords to be swapped
segcoords = [[(c[1], c[0]) for c in seg] for seg in segcoords]
connectors = [[(c[1], c[0]) for c in con] for con in connectors]

linestring = MultiLineString(segcoords)
connectorstring = MultiLineString(connectors)
feature = Feature(geometry=linestring)
connectorfeature = Feature(geometry=connectorstring)
features = FeatureCollection([feature, connectorfeature])
json = geojson.dumps(features)

ofile = open("../webgui/output.json","w")

ofile.write(json)
ofile.close()
