from stravalib import Client
from tokens_file import *


client = Client(access_token=ACCESS_TOKEN)
athlete = client.get_athlete()

bound = [40.472794,-105.153343,40.639351,-104.982079]
smallbound = [40.472794,-105.153343,40.55,-105.05]

#whaleSegID = 14411824
#whaleSeg = client.get_segment(whaleSegID)

print(athlete)


#print("=========")
#print(whaleSeg)

print("=========")
#focoSegs = client.explore_segments(bound)
#print(focoSegs)

segmentlist = []
def collectRecursive(bounds):	
    segs = client.explore_segments(bounds)

    print("\nExploring box, found segments:")
    print(bounds)
    print(segs)
    print(len(segs))
    if len(segs) < 10:
        return segs

    width = bounds[3] - bounds[1]
    height = bounds[2] - bounds[0]

    
    
    segments = []
    if(width > height):
        segments.extend(collectRecursive([bounds[0], bounds[1], bounds[2], bounds[1] + width/2]))
        segments.extend(collectRecursive([bounds[0], bounds[3] - width/2, bounds[2], bounds[3]]))
    else:
        segments.extend(collectRecursive([bounds[0], bounds[1], bounds[0] + height/2, bounds[3]]))
        segments.extend(collectRecursive([bounds[2] - height/2, bounds[1], bounds[2], bounds[3]]))


    return segments

segmentlist = collectRecursive(bound)

print(segmentlist)
print(len(segmentlist))

