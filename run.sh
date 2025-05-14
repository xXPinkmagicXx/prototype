#! /bin/bash

# Run the grpc experiments

# Create experiments
for value in 100 1000 10000; do
   python main.py -g -s -n $value -m create
done

# Get experiment
for value in 100 1000 10000; do
   python main.py -g -s -n $value -m get 
done

# Run the REST experiments
for value in 100 1000 10000; do
   python main.py -r -s -n $value -m create 
done

for value in 100 1000 10000; do
   python main.py -r -s -n $value -m get 
done
