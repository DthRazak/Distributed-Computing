#!/bin/bash

hdfs dfs -mkdir -p /Integer-Operations/input
hdfs dfs -mkdir -p /Integer-Operations/output1
hdfs dfs -mkdir -p /Integer-Operations/output2

echo "Copying input file..."
hdfs dfs -put -f ../../input/data.txt /Integer-Operations/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Integer-Operations/output1
hdfs dfs -rm -r /Integer-Operations/output2

echo "Starting computations..."

# Split parameter
NUM_SPLIT=5

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator=';' \
    -D stream.reduce.input.field.separator=';' \
    -mapper "python3 ./mapper1.py ${NUM_SPLIT}" \
    -reducer "python3 ./reducer1.py" \
    -input "/Integer-Operations/input/data.txt" \
    -output "/Integer-Operations/output1" \

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator=';' \
    -D stream.reduce.input.field.separator=';' \
    -mapper "python3 ./mapper2.py" \
    -reducer "python3 ./reducer2.py" \
    -input "/Integer-Operations/output1/part-00000" \
    -output "/Integer-Operations/output2" \

echo "Copying result file..."
hdfs dfs -get -f /Integer-Operations/output1/part-00000 \
    ../../output/hadoop-python-find-maximum.txt
