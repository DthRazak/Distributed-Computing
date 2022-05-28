#!/bin/bash

hdfs dfs -mkdir -p /Integer-Operations/input
hdfs dfs -mkdir -p /Integer-Operations/output1

echo "Copying input file..."
hdfs dfs -put -f ../../input/data.txt /Integer-Operations/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Integer-Operations/output1

echo "Starting computations..."

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator=';' \
    -D stream.reduce.input.field.separator=';' \
    -mapper "python3 ./mapper.py" \
    -reducer "python3 ./reducer.py" \
    -input "/Integer-Operations/input/data.txt" \
    -output "/Integer-Operations/output1" \

echo "Copying result file..."
#hdfs dfs -get -f /Integer-Operations/output1/part-00000 \
#    ../../output/hadoop-python-filter-duplicates.txt
hdfs dfs -get -f /Integer-Operations/output1/part-00000 \
    /tmp/hadoop-python-filter-duplicates.txt
