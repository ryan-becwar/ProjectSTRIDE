from collector import *

def dist(lat, lon, tarlat, tarlon):
    lat_dif = (lat - tarlat) * M_PER_LAT
    lon_dif = (lon - tarlon) * M_PER_LON

    return math.sqrt((lat_dif ** 2) + (lon_dif ** 2))

def route(lat, lon, distance, segments):

    
    return 

def goal(segid, targetlat, targetlon, threshold, segments):
    seg = segments[segid]
    lat = seg.end_latitude
    lon = seg.end_longitude

    return(dist(lat, lon, targetlat, targetlon) < threshold)
    
#Breadth first search generator which returns all possible paths that end within range of target
#location which do not exceed cutoff in total distance
def bfs_paths(startsegid, targetlat, targetlon, threshold, segments, cutoff):
    queue = [(startsegid, [startsegid], segments[startsegid].distance)]
    while queue:
        (vertex, path, distance) = queue.pop(0)
        vertseg = segments[vertex]
        for next in set(vertseg.links) - set(path):
            #only add further segments while the distance threshold has not been exceeded
            nextseg = segments[next]
            newdist = distance + segments[next].distance + dist(vertseg.end_latitude, vertseg.end_longitude, nextseg.start_latitude, nextseg.start_longitude)
            if newdist <= cutoff:
                if goal(next, targetlat, targetlon, threshold, segments):
                    yield path + [next]
                else:
                    queue.append((next, path + [next], newdist))


#function to search from a segment to a geographic point on the graph
def search(startsegid, targetlat, targetlon, threshold, segments, cutoffratio):
    cutoff = dist(segments[startsegid].start_latitude, segments[startsegid].start_longitude, targetlat, targetlon) * cutoffratio
    bestpath = []
    bestscore = 0.0
    for path in bfs_paths(startsegid, targetlat, targetlon, threshold, segments, cutoff):
        score = evalPath(path, segments)
        if score > bestscore:
            bestpath = path
            bestscore = score
        print(path, score)
        
        #keep track of highest scoring path
    return bestpath

#Gives a score for a given path.
def evalPath(path, segments):
    #should expand upon this, star count will do for now
    starcount = 0.0
    for seg in path:
        starcount += segments[seg].star_count

    return starcount

def run(segmentsfile, distance):
    segments = load_segments_dictionary(segmentsfile)

    #route = route(40.5, -105, segments)
    #print(route)

    #test specifically for tiny dataset
    path = search(5660941, 40.475605, -105.148393, 10, segments, 50.0)
    print(path)


if __name__ == "__main__":
    run("tinyColorado.json")
