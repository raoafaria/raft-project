#!/bin/bash

# Define the number of nodes for the cluster
NUM_NODES=5

# Create a custom Docker network for the cluster
docker network create raft-cluster

# Build the Java Docker image
echo "Building Java Docker image..."
docker build -t raft-java-node -f docker/java-node.Dockerfile .

# Build the Python Docker image
echo "Building Python Docker image..."
docker build -t raft-python-node -f docker/python-node.Dockerfile .

# Start the Java and Python nodes
for i in $(seq 1 $NUM_NODES); do
  if (( $i % 2 == 0 )); then
    echo "Starting Java node $i..."
    docker run -d --name java-node-$i --network raft-cluster raft-java-node
  else
    echo "Starting Python node $i..."
    docker run -d --name python-node-$i --network raft-cluster raft-python-node
  fi
done

# Wait for the nodes to start
echo "Waiting for nodes to initialize..."
sleep 10

# Verify the running containers
echo "Running nodes:"
docker ps

# Optionally print the logs of all nodes
for i in $(seq 1 $NUM_NODES); do
  if (( $i % 2 == 0 )); then
    docker logs java-node-$i
  else
    docker logs python-node-$i
  fi
done

echo "Raft cluster started successfully!"
