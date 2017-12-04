from stravalib import Client
import json
from tokens_file import *
import math as math
from time import sleep


client = Client(access_token=ACCESS_TOKEN)

front_range = [37.9788,-105.6445,40.9716,-102.041]
norther_colorado = [40.2837,-105.6665,40.8865,-104.5569]
greater_fortcollins = [40.423951,-105.24559,40.735812,-104.831543]
bound = [40.472794,-105.153343,40.639351,-104.982079]
smallbound = [40.472794,-105.153343,40.55,-105.05]
tinybound = [40.472794,-105.153343,40.5,-105.1]


#40.5 is the average latitude over the distance... this should be calculated but as our use case is always in the same
#general latitude this is fine, and saves computational time which is more crucial than accuracy
M_PER_LAT = 111132.954 - 559.822 * math.cos( 2.0 * 40.5 ) + 1.175 * math.cos( 4.0 * 40.5)
M_PER_LON = (3.14159265359/180 ) * 6367449 * math.cos( 40.5 )
LAT_PER_M = 1.0 / M_PER_LAT
LON_PER_M = 1.0 / M_PER_LON
DIST_CUTOFF = 1000 #meters
SLEEP = True

class Segment:

    def __init__(self, lat, lon):
        self.id = 1
        self.name = "Start Segment"
        self.distance = 0
        obj.total_elevation_gain =  0
        obj.climbing_ratio = 0
        obj.maximum_grade = 0
        obj.start_latitude = lat
        obj.end_latitude = lat
        obj.start_longitude = lon
        obj.end_longitude = lon
        obj.effort_count = 0
        obj.athlete_count = 0
        obj.star_count = 0
        obj.polyline = ""
        obj.links = []


    @classmethod
    def fromstrava(cls, stra):
        obj = cls()
        obj.id = stra.id
        obj.name = stra.name
        obj.distance = float(stra.distance)
        obj.total_elevation_gain = float(stra.total_elevation_gain)
        obj.climbing_ratio = obj.total_elevation_gain / obj.distance
        obj.maximum_grade = stra.maximum_grade
        obj.start_latitude = stra.start_latitude
        obj.end_latitude = stra.end_latitude
        obj.start_longitude = stra.end_longitude
        obj.end_longitude = stra.end_longitude
        obj.effort_count = stra.effort_count
        obj.athlete_count = stra.athlete_count
        obj.star_count = stra.star_count
        obj.polyline = stra.map.polyline
        obj.links = []
        return obj
    
    @classmethod
    def fromdict(cls, segdict):
        obj = cls()
        obj.id = segdict['id']
        obj.name = segdict['name']
        obj.distance = segdict['distance']
        obj.total_elevation_gain = segdict['total_elevation_gain']
        obj.climbing_ratio = segdict['climbing_ratio']
        obj.maximum_grade = segdict['maximum_grade']
        obj.start_latitude = segdict['start_latitude']
        obj.end_latitude = segdict['end_latitude']
        obj.start_longitude = segdict['end_longitude']
        obj.end_longitude = segdict['end_longitude']
        obj.effort_count = segdict['effort_count']
        obj.athlete_count = segdict['athlete_count']
        obj.star_count = segdict['star_count']
        if 'polyline' in segdict:
            obj.polyline = segdict['polyline']
        else:
            obj.polyline = None
        if 'links' in segdict:
            obj.links = segdict['links']
        else:
            obj.links = []
        return obj

    def dist(self, segment):
        lat_dif = (self.end_latitude - segment.start_latitude) * M_PER_LAT
        lon_dif = (self.end_longitude - segment.start_longitude) * M_PER_LON

        return math.sqrt((lat_dif ** 2) + (lon_dif ** 2))

def load_segments_json(jsonfile):
    data_file = open(jsonfile).read()
    loaded = []
    data = json.loads(data_file)
    for item in data:
        loaded.append(Segment.fromdict(item))

    return loaded

def load_segments_dictionary(jsonfile):
    data_file = open(jsonfile).read()
    loaded = {}
    data = json.loads(data_file)
    for item in data:
        seg = Segment.fromdict(item)
        loaded[seg.id] = seg

    return loaded

def write_segments_json(jsonfile, segmentlist):
    jsonOut = json.dumps([seg.__dict__ for seg in segmentlist])

    with open(jsonfile, "w") as text_file:
        text_file.write(jsonOut)

def add_links(segments):
    for seg in segments:
        seg.links = []
        for seg2 in segments:
            if seg != seg2:
                if seg.dist(seg2) <= DIST_CUTOFF:
                    seg.links.append(seg2.id)

def collectRecursive(bounds, segments):	
    segs = client.explore_segments(bounds)
    if SLEEP:
        sleep(1.50)

    print("\nExploring box, found segments:")
    print(bounds)
    print(segs)
    print(len(segs))
    if len(segs) < 10:
        fullsegs = []
        for seg in segs:
            fullsegs.append(Segment.fromstrava(seg.segment))
            if SLEEP:
                sleep(1.50)

        #build the links attribute of the segments
        for seg in fullsegs:
            for seg2 in fullsegs:
                if seg != seg2:
                    if seg.dist(seg2) <= DIST_CUTOFF:
                        seg.links.append(seg2.id)
            for seg2 in segments:
                if seg != seg2:
                    if seg.dist(seg2) <= DIST_CUTOFF:
                        seg.links.append(seg2.id)

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

def collect_segments(bounds, fileout):
    segmentlist = []
    collectRecursive(bounds, segmentlist)
    print(len(segmentlist))

    write_segments_json(fileout, segmentlist)

if __name__ == "__main__":
    collect_segments(tinybound, "testout.json")

