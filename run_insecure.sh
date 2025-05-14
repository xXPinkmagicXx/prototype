#! /bin/bash



# Run the grpc experiments
# Create experiments Insecure
for value in 100 1000 10000; do
   python main.py -g -n $value -m create
done

# grcp get experiment 
for value in 100 1000 10000; do
   python main.py -g -n $value -m get 
done

# Run the REST create experiments 
for value in 100 1000 10000; do
   python main.py -r -n $value -m create 
done

# Run the REST create experiments
for value in 100 1000 10000; do
   python main.py -r -n $value -m get 
done
