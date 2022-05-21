#!/bin/bash

hdfs dfs -mkdir -p /Word-Count/input
hdfs dfs -mkdir -p /Word-Count/output

echo "Copying input file..."
hdfs dfs -put -f ../input/text.txt /Word-Count/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Word-Count/output

echo "Starting computations..."

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -mapper "python3 ./mapper.py" \
    -reducer "python3 ./reducer.py" \
    -input "/Word-Count/input/text.txt" \
    -output "/Word-Count/output"

echo "Copying result file..."
hdfs dfs -get -f /Word-Count/output/part-00000 ../output/hadoop-python-result.txt
