#!/bin/bash

hdfs dfs -mkdir -p /Terasort/input
hdfs dfs -mkdir -p /Terasort/output1
hdfs dfs -mkdir -p /Terasort/output2
hdfs dfs -mkdir -p /Terasort/output3

echo "Copying input file..."
hdfs dfs -put -f ../input/data.txt /Terasort/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Terasort/output1
hdfs dfs -rm -r /Terasort/output2
hdfs dfs -rm -r /Terasort/output3

echo "Starting computations..."

P=10
N=1000

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator='|' \
    -D stream.reduce.input.field.separator='|' \
    -mapper "python3 ./mapper1.py ${P} ${N}" \
    -reducer "python3 ./reducer1.py" \
    -input "/Terasort/input/data.txt" \
    -output "/Terasort/output1" \

ETA=$(hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator='|' \
    -D stream.reduce.input.field.separator='|' \
    -mapper "python3 ./mapper2.py" \
    -reducer "python3 ./reducer2.py" \
    -input "/Terasort/output1/part-00000" \
    -output "/Terasort/output2" 2>&1 | grep 'Reduce input groups=' | tail -1 | cut -d "=" -f 2-)

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator='|' \
    -D stream.reduce.input.field.separator='|' \
    -mapper "python3 ./mapper3.py ${ETA}" \
    -reducer "python3 ./reducer3.py" \
    -input "/Terasort/output2/part-00000" \
    -output "/Terasort/output3" \

echo "Copying result file..."
hdfs dfs -get -f /Terasort/output2/part-00000 \
    ../../output/hadoop-python-result.txt
