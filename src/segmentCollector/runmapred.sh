$HADOOP_HOME/bin/hdfs dfs -rm -r /out.txt 
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar -files mapper.py,reducer.py -mapper 'mapper.py /FortCollinsFixed.json 40.574375 -105.100806 10000 1600' -reducer reducer.py -input /FortCollinsFixed.json -output /out.txt

