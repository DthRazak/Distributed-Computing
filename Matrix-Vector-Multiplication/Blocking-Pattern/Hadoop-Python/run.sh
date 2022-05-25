#!/bin/bash

hdfs dfs -mkdir -p /Matrix-Vector-Multiplication/input
hdfs dfs -mkdir -p /Matrix-Vector-Multiplication/output1
hdfs dfs -mkdir -p /Matrix-Vector-Multiplication/output2

echo "Copying input file..."
hdfs dfs -put -f ../../input/mat_20.txt /Matrix-Vector-Multiplication/input/

echo "Clearing output dir from previous run..."
hdfs dfs -rm -r /Matrix-Vector-Multiplication/output1
hdfs dfs -rm -r /Matrix-Vector-Multiplication/output2

echo "Starting computations..."

N=20;
BLOCK_SIZE=5;

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator='|' \
    -D stream.reduce.input.field.separator='|' \
    -mapper "python3 ./mapper1.py ${N} ${BLOCK_SIZE}" \
    -reducer "python3 ./reducer1.py" \
    -input "/Matrix-Vector-Multiplication/input/mat_20.txt" \
    -output "/Matrix-Vector-Multiplication/output1" \

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.2.jar \
    -D stream.map.output.field.separator=';' \
    -D stream.reduce.input.field.separator=';' \
    -mapper "python3 ./mapper2.py" \
    -reducer "python3 ./reducer2.py" \
    -input "/Matrix-Vector-Multiplication/output1/part-00000" \
    -output "/Matrix-Vector-Multiplication/output2" \

echo "Copying result file..."
hdfs dfs -get -f /Matrix-Vector-Multiplication/output2/part-00000 \
    ../../output/hadoop-python-result-striping.txt
