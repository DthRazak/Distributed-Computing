#!/bin/bash

hdfs dfs -mkdir -p /Matrix-Matrix-Multiplication/input
hdfs dfs -mkdir -p /Matrix-Matrix-Multiplication/output1
hdfs dfs -mkdir -p /Matrix-Matrix-Multiplication/output2

echo "Copying input file..."
hdfs dfs -put -f ../../input/data.txt /Matrix-Matrix-Multiplication/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Matrix-Matrix-Multiplication/output1
hdfs dfs -rm -r /Matrix-Matrix-Multiplication/output2

echo "Starting computations..."

# Size of Matrices: A(N x P) and B(P x M)
N=20
P=20
M=20

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator='|' \
    -D stream.reduce.input.field.separator='|' \
    -mapper "python3 ./mapper.py ${N} ${M}" \
    -reducer "python3 ./reducer.py ${P}" \
    -input "/Matrix-Matrix-Multiplication/input/data.txt" \
    -output "/Matrix-Matrix-Multiplication/output1" \

echo "Copying result file..."
#hdfs dfs -get -f /Matrix-Matrix-Multiplication/output1/part-00000 \
#    ../../output/hadoop-python-single-round.txt
hdfs dfs -get -f /Matrix-Matrix-Multiplication/output1/part-00000 \
    /tmp/hadoop-python-single-round.txt
