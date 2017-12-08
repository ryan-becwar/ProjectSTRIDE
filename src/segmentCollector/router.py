from collector import *
import random


def dist(lat, lon, tarlat, tarlon):
    lat_dif = (lat - tarlat) * M_PER_LAT
    lon_dif = (lon - tarlon) * M_PER_LON

    return math.sqrt((lat_dif ** 2) + (lon_dif ** 2))

#individual route search, finds 
def route(lat, lon, distance, threshold, segments, cutoffratio):

    #a random direction, and a second +- 60 degrees
    dir_radians = random.uniform(0.0, 2.0*math.pi)
    dir2_radians = (dir_radians + random.choice([-1.0, 1.0]) * math.pi / 3.0) % (2.0 * math.pi)

    length = distance / 3.0
    x1off = length * math.cos(dir_radians) * LON_PER_M
    y1off = length * math.sin(dir_radians) * LAT_PER_M
    x2off = length * math.cos(dir2_radians) * LON_PER_M
    y2off = length * math.sin(dir2_radians) * LAT_PER_M

    lon1 = lon + x1off
    lat1 = lat + y1off
    lon2 = lon + x2off
    lat2 = lat + y2off

    #TODO: find solution to make dummy start searchable by path algorithm one option would be hardcode check for id 1
    #solution: add dummy segment with constant id 1, add to dict, remove 1st segment of route when route is returned, which is dummy
    dummy_start = Segment.dummy(lat, lon)
    for seg in segments:
        if dist(lat, lon, segments[seg].start_latitude, segments[seg].start_longitude) <= threshold:
            dummy_start.links.append(seg)
    segments[1] = dummy_start

    path1 = search(dummy_start.id, lat1, lon1, threshold, segments, cutoffratio, set([]))[1:]#remove first elem
    if not path1:
        return []
    path2 = search(path1[-1], lat2, lon2, threshold, segments, cutoffratio, set(path1))[1:]
    if not path2:
        return []
    path3 = search(path2[-1], lat, lon, threshold, segments, cutoffratio, set(path1) | set(path2))[1:]
    if not path3:
        return []

    path1.extend(path2)
    path1.extend(path3)
    return path1

def goal(segid, targetlat, targetlon, threshold, segments):
    seg = segments[segid]
    lat = seg.end_latitude
    lon = seg.end_longitude

    return(dist(lat, lon, targetlat, targetlon) < threshold)
    
#Breadth first search generator which returns all possible paths that end within range of target
#location which do not exceed cutoff in total distance
def bfs_paths(startsegid, targetlat, targetlon, threshold, segments, cutoff, visited):
    queue = [(startsegid, [startsegid], segments[startsegid].distance)]
    while queue:
        (vertex, path, distance) = queue.pop(0)
        vertseg = segments[vertex]
        for next in set(vertseg.links) - set(path) - visited:
            #only add further segments while the distance threshold has not been exceeded
            nextseg = segments[next]
            newdist = distance + segments[next].distance + dist(vertseg.end_latitude, vertseg.end_longitude, nextseg.start_latitude, nextseg.start_longitude)
            if newdist <= cutoff:
                if goal(next, targetlat, targetlon, threshold, segments):
                    yield (path + [next], newdist)
                else:
                    queue.append((next, path + [next], newdist))


#function to search from a segment to a geographic point on the graph
def search(startsegid, targetlat, targetlon, threshold, segments, cutoffratio, visited):
    cutoff = dist(segments[startsegid].start_latitude, segments[startsegid].start_longitude, targetlat, targetlon) * cutoffratio
    bestpath = []
    bestscore = -1.0
    for path in bfs_paths(startsegid, targetlat, targetlon, threshold, segments, cutoff, visited):
        score = evalPath(path[0], segments)
        if score > bestscore:
            bestpath = path[0]
            bestscore = score
        #print(path[0], score, path[1])
        
        #keep track of highest scoring path
    return bestpath

#Gives a score for a given path.
def evalPath(path, segments):
    #should expand upon this, star count will do for now
    starcount = 0.0
    riders = 0.0
    for seg in path:
        #starcount += segments[seg].star_count
        starcount += segments[seg].athlete_count * segments[seg].distance
        segment = segments[seg]
        if segment.athlete_count > 0 and segment.distance > 0:
            riders += (segment.effort_count / segment.athlete_count) * segment.distance



    return starcount + 0.5 + riders

def run(segmentsstring, lat, lon, distance, threshold, cutoffratio=1.5):
    #segments = load_segments_dictionary(segmentsfile)
    segments = segments_dictionary(segmentsstring)


    #testroute = route(40.55, -105.10, distance, threshold,  segments, cutoffratio)
    testroute = route(lat, lon, distance, threshold,  segments, cutoffratio)
    #print(testroute)
    coords = []
    for seg in testroute:
        coords.append(((segments[seg].start_latitude, segments[seg].start_longitude), (segments[seg].end_latitude, segments[seg].end_longitude), segments[seg].polyline))
    #print(coords)


    return (coords, evalPath(testroute, segments))
    #test specifically for tiny dataset
    #path = search(5660941, 40.475605, -105.148393, 10, segments, cutoffratio)
    #print(path)


if __name__ == "__main__":
    run("tinyColorado.json")
