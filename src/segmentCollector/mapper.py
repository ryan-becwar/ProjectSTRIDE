#!/usr/local/anaconda/bin/python

import sys
import subprocess
#import random
from router import *

datafile = sys.argv[1]
lat = sys.argv[2]
lon = sys.argv[3]
dist = sys.argv[4]
threshold = sys.argv[5]

# Read each line from STDIN
data = sys.stdin.read()


# Get the words in each line
#cat = subprocess.Popen(["/usr/local/hadoop/bin/hdfs", "dfs", "-cat", datafile], stdout=subprocess.PIPE)
#data = cat.stdout.read()

#data = open("/s/chopin/l/grad/rbecwar/code/ProjectStride/src/segmentCollector/data/FortCollinsFixed.json").read()


#data = open(datafile).read()
# Generate the count for each word
#for word in words:
for i in range(500):

    output = run(data, float(lat), float(lon), float(dist), float(threshold))

    #key = random.randint(0, sys.maxsize)

    # Write the key-value pair to STDOUT to be processed by the reducer.
    # The key is anything before the first tab character and the value is
    # anything after the first tab character.
    print('{0}\t{1}'.format(i, output))
