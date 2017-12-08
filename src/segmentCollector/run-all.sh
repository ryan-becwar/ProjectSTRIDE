./runmapred.sh

rm part-00000
$HADOOP_HOME/bin/hdfs dfs -get /out.txt/part-00000

python formatoutput.py

