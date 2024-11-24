import grpc
from concurrent import futures
import time
import random
import raft_pb2
import raft_pb2_grpc


class RaftNode(raft_pb2_grpc.RaftNodeServicer):
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.state = "Follower"
        self.current_term = 0
        self.voted_for = None
        self.timeout = random.randint(150, 300) / 1000.0  # Election timeout in seconds
        self.last_heartbeat = time.time()
        self.is_leader = False
        self.vote_count = 0
        self.log = []  # To store log entries

    def RequestVote(self, request, context):
        print(f"Process {self.node_id} receives RPC RequestVote from Process {request.candidateId}")
        response = raft_pb2.VoteResponse(term=self.current_term, voteGranted=False)

        if request.term > self.current_term:
            self.current_term = request.term
            self.voted_for = None

        if self.voted_for is None or self.voted_for == request.candidateId:
            response.voteGranted = True
            self.voted_for = request.candidateId
            self.last_heartbeat = time.time()

        return response

    def AppendEntries(self, request, context):
        print(f"Process {self.node_id} receives RPC AppendEntries from Process {request.leaderId}")
        self.last_heartbeat = time.time()
        self.state = "Follower"

        # Append new entries to the log
        self.log.extend(request.entries)

        return raft_pb2.AppendEntriesResponse(term=self.current_term, success=True)

    def ExecuteOperation(self, request, context):
        print(f"Process {self.node_id} receives RPC ExecuteOperation from client with operation {request.operation}")

        # Create a new log entry for the operation
        log_entry = raft_pb2.LogEntry(index=len(self.log) + 1, term=self.current_term, operation=request.operation)
        self.log.append(log_entry)

        # Normally, we would wait for the operation to be committed, but here we'll return an immediate success for simplicity.
        response = raft_pb2.ExecuteOperationResponse(success=True)

        return response

    def run(self):
        while True:
            time.sleep(0.1)  # Simulate event loop
            if self.state == "Follower" and time.time() - self.last_heartbeat > self.timeout:
                print(f"Process {self.node_id} transitioning to Candidate")
                self.state = "Candidate"
                self.start_election()

    def start_election(self):
        self.current_term += 1
        self.voted_for = self.node_id
        self.vote_count = 1  # Vote for self
        print(f"Process {self.node_id} starts an election for term {self.current_term}")

        for peer in self.peers:
            try:
                with grpc.insecure_channel(f'localhost:500{peer}') as channel:
                    grpc.channel_ready_future(channel).result(timeout=2)
                    stub = raft_pb2_grpc.RaftNodeStub(channel)
                    request = raft_pb2.RequestVoteRequest(term=self.current_term, candidateId=self.node_id)
                    print(f"Process {self.node_id} sends RPC RequestVote to Process {peer}")
                    response = stub.RequestVote(request)
                    if response.voteGranted:
                        self.vote_count += 1
            except grpc.FutureTimeoutError:
                print(f"Process {self.node_id} could not establish a connection with Process {peer} (timeout).")
                continue

        if self.vote_count > len(self.peers) // 2:  # Majority
            print(f"Process {self.node_id} becomes the Leader for term {self.current_term}")
            self.state = "Leader"
            self.is_leader = True
            self.send_heartbeats()

    def send_heartbeats(self):
        while self.is_leader:
            for peer in self.peers:
                try:
                    with grpc.insecure_channel(f'localhost:500{peer}') as channel:
                        stub = raft_pb2_grpc.RaftNodeStub(channel)
                        entries = [
                            raft_pb2.LogEntry(index=len(self.log), term=self.current_term, operation="heartbeat")]
                        request = raft_pb2.AppendEntriesRequest(term=self.current_term, leaderId=self.node_id,
                                                                entries=entries)
                        print(f"Process {self.node_id} sends RPC AppendEntries to Process {peer}")
                        stub.AppendEntries(request)
                except Exception as e:
                    print(f"Process {self.node_id} failed to contact Process {peer}: {e}")
            time.sleep(0.1)  # Heartbeat interval


def serve(node_id, peers):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node = RaftNode(node_id, peers)
    raft_pb2_grpc.add_RaftNodeServicer_to_server(node, server)
    server.add_insecure_port(f'[::]:500{node_id}')
    server.start()
    print(f"Process {node_id} started and listening on port 500{node_id}")
    node.run()


if __name__ == "__main__":
    import sys

    node_id = int(sys.argv[1])
    peers = [1, 2, 3, 4, 5]
    peers.remove(node_id)
    serve(node_id, peers)
