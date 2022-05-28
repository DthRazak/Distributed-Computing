#!/bin/bash

hdfs dfs -mkdir -p /Matrix-Matrix-Multiplication/input
hdfs dfs -mkdir -p /Matrix-Matrix-Multiplication/output1

echo "Copying input file..."
hdfs dfs -put -f ../../input/data.txt /Matrix-Matrix-Multiplication/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Matrix-Matrix-Multiplication/output1

echo "Starting computations..."

# Size of square Matrices (N) A and B
N=20
BAND_NUMBER=5

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator='|' \
    -D stream.reduce.input.field.separator='|' \
    -mapper "python3 ./mapper.py ${N} ${BAND_NUMBER}" \
    -reducer "python3 ./reducer.py" \
    -input "/Matrix-Matrix-Multiplication/input/data.txt" \
    -output "/Matrix-Matrix-Multiplication/output1" \

echo "Copying result file..."
#hdfs dfs -get -f /Matrix-Matrix-Multiplication/output1/part-00000 \
#    ../../output/hadoop-python-banding-pattern.txt
hdfs dfs -get -f /Matrix-Matrix-Multiplication/output1/part-00000 \
    /tmp/hadoop-python-banding-pattern.txt
