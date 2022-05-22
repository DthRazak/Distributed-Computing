#!/bin/bash

hdfs dfs -mkdir -p /Word-Mean/input
hdfs dfs -mkdir -p /Word-Mean/output

echo "Copying input file..."
hdfs dfs -put -f ../input/text.txt /Word-Mean/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Word-Mean/output

echo "Starting computations..."

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -mapper "python3 ./mapper.py" \
    -reducer "python3 ./reducer.py" \
    -input "/Word-Mean/input/text.txt" \
    -output "/Word-Mean/output"

echo "Copying result file..."
#hdfs dfs -get -f /Word-Mean/output/part-00000 ../output/hadoop-python-result.txt
hdfs dfs -get -f /Word-Mean/output/part-00000 /tmp/hadoop-python-result.txt
