# Folder Structure
raft-project
/docker[docket setup-incomplete] /java-code[java implementation] /proto[proto file] /python-code[python implementation] /scripts[cluster conf-incomplete]

# Python Implementation

Below is the instruction to impeplement gRPC and Raft in python.
In Folder 'Python-Node'
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install grpcio grpcio-tools
```

## Generate gRPC Stubs
```bash
 python -m grpc_tools.protoc -I../proto/ --python_out=./src --pyi_out=./src --grpc_python_out=./src ../proto/raft.proto
```

## Run node.py [Server]
Terminal 1
```bash
python node.py 1
Process 1 started and listening on port 5001
Process 1 transitioning to Candidate
Process 1 starts an election for term 1
Process 1 sends RPC RequestVote to Process 2
Process 1 sends RPC RequestVote to Process 3
Process 1 sends RPC RequestVote to Process 4
Process 1 could not establish a connection with Process 5 (timeout).
...
```
Terminal 2
```bash
python node.py 2
Process 2 started and listening on port 5002
Process 2 transitioning to Candidate
Process 2 starts an election for term 1
Process 2 sends RPC RequestVote to Process 1
Process 2 sends RPC RequestVote to Process 3
Process 2 sends RPC RequestVote to Process 4
Process 2 could not establish a connection with Process 5 (timeout).
Process 2 receives RPC RequestVote from Process 1
...
```
Terminal 3
```bash
python client.py
Enter the node ID you want to connect to: 1
Enter the operation to send: write
Client: Operation 'write' successfully added to log.
...
```
Termial 1 should show this now.
```bash
python node.py 1
Process 1 started and listening on port 5001
Process 1 transitioning to Candidate
Process 1 starts an election for term 1
Process 1 sends RPC RequestVote to Process 2
Process 1 sends RPC RequestVote to Process 3
Process 1 sends RPC RequestVote to Process 4
Process 1 could not establish a connection with Process 5 (timeout).
Process 1 receives RPC ExecuteOperation from client with operation write
```

# Java Implementation
Below is the instruction to impeplement gRPC and Raft in Java.
In Folder 'Java-Node'
```bash
mvn clean install
```
```bash
mvn clean package
```
```bash
java -jar target/java-node-1.0-SNAPSHOT.jar 3
Process 3 started, listening on port 5003
Process 3 transitioning to Candidate
Process 3 starts election for term 1
Process 3 sends RequestVote to Process 4
Process 3 sends RequestVote to Process 5
Process 3 sends RequestVote to Process 1
Process 3 sends RequestVote to Process 2
Process 3 failed to contact Process 1: UNKNOWN
Process 3 failed to contact Process 5: UNKNOWN
Process 3 failed to contact Process 4: UNKNOWN
Process 3 failed to contact Process 2: UNKNOWN

```