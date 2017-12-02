from stravalib import Client
import json
from tokens_file import *


client = Client(access_token=ACCESS_TOKEN)


greater_fortcollins = [40.423951,-105.24559,40.735812,-104.831543]
bound = [40.472794,-105.153343,40.639351,-104.982079]
smallbound = [40.472794,-105.153343,40.55,-105.05]
tinybound = [40.472794,-105.153343,40.5,-105.1]

class Segment:

    def __init__(self, stra):
        self.id = stra.id
        self.name = stra.name
        self.distance = float(stra.distance)
        self.total_elevation_gain = float(stra.total_elevation_gain)
        self.climbing_ratio = self.total_elevation_gain / self.distance
        self.maximum_grade = stra.maximum_grade
        self.start_latitude = stra.start_latitude
        self.end_latitude = stra.end_latitude
        self.start_longitude = stra.end_longitude
        self.end_longitude = stra.end_longitude
        self.effort_count = stra.effort_count
        self.athlete_count = stra.athlete_count
        self.star_count = stra.star_count

#helper function to help with serialization
def obj_dict(obj):
    return obj.__dict__

def collectRecursive(bounds, segments):	
    segs = client.explore_segments(bounds)

    print("\nExploring box, found segments:")
    print(bounds)
    print(segs)
    print(len(segs))
    if len(segs) < 10:
        fullsegs = []
        for seg in segs:
            fullsegs.append(Segment(seg.segment))
        segments.extend(fullsegs)
        return

    width = bounds[3] - bounds[1]
    height = bounds[2] - bounds[0]
    
    if(width > height):
        collectRecursive([bounds[0], bounds[1], bounds[2], bounds[1] + width/2], segments)
        collectRecursive([bounds[0], bounds[3] - width/2, bounds[2], bounds[3]], segments)
    else:
        collectRecursive([bounds[0], bounds[1], bounds[0] + height/2, bounds[3]], segments)
        collectRecursive([bounds[2] - height/2, bounds[1], bounds[2], bounds[3]], segments)



segmentlist = []
collectRecursive(greater_fortcollins, segmentlist)


jsonOut = json.dumps([seg.__dict__ for seg in segmentlist])
print(jsonOut)

with open("GreaterFortCollinsSegments.json", "w") as text_file:
    text_file.write(jsonOut)

    

