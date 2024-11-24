package com.example.raft;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;

import java.io.IOException;
import java.util.*;
import java.util.concurrent.*;

public class Node extends RaftNodeGrpc.RaftNodeImplBase {
    private final int nodeId;
    private final List<Integer> peers;
    private String state = "Follower";
    private int currentTerm = 0;
    private Integer votedFor = null;
    private final Random random = new Random();
    private final double timeout = (150 + random.nextInt(150)) / 1000.0; // Election timeout
    private long lastHeartbeat = System.currentTimeMillis();
    private boolean isLeader = false;
    private int voteCount = 0;
    private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);

    public Node(int nodeId, List<Integer> peers) {
        this.nodeId = nodeId;
        this.peers = peers;
    }

    @Override
    public void requestVote(RequestVoteRequest request, StreamObserver<VoteResponse> responseObserver) {
        System.out.printf("Process %d received RequestVote from Process %d%n", nodeId, request.getCandidateId());
        VoteResponse.Builder response = VoteResponse.newBuilder().setTerm(currentTerm).setVoteGranted(false);

        if (request.getTerm() > currentTerm) {
            currentTerm = request.getTerm();
            votedFor = null;
        }

        if ((votedFor == null || votedFor.equals(request.getCandidateId())) && request.getTerm() >= currentTerm) {
            response.setVoteGranted(true);
            votedFor = request.getCandidateId();
            lastHeartbeat = System.currentTimeMillis();
        }

        responseObserver.onNext(response.build());
        responseObserver.onCompleted();
    }

    @Override
    public void appendEntries(AppendEntriesRequest request, StreamObserver<AppendEntriesResponse> responseObserver) {
        System.out.printf("Process %d received AppendEntries from Leader %d%n", nodeId, request.getLeaderId());
        lastHeartbeat = System.currentTimeMillis();
        state = "Follower";
        responseObserver.onNext(AppendEntriesResponse.newBuilder().setTerm(currentTerm).setSuccess(true).build());
        responseObserver.onCompleted();
    }

    public void startElection() {
        currentTerm++;
        votedFor = nodeId;
        voteCount = 1; // Vote for self
        System.out.printf("Process %d starts election for term %d%n", nodeId, currentTerm);

        for (int peer : peers) {
            final int peerId = peer;
            CompletableFuture.runAsync(() -> {
                try {
                    RaftNodeGrpc.RaftNodeBlockingStub stub = createStub(peerId);
                    RequestVoteRequest request = RequestVoteRequest.newBuilder()
                            .setTerm(currentTerm)
                            .setCandidateId(nodeId)
                            .build();

                    System.out.printf("Process %d sends RequestVote to Process %d%n", nodeId, peerId);
                    VoteResponse response = stub.requestVote(request);
                    if (response.getVoteGranted()) {
                        synchronized (this) {
                            voteCount++;
                            if (voteCount > peers.size() / 2 && !isLeader) {
                                isLeader = true;
                                state = "Leader";
                                System.out.printf("Process %d becomes Leader for term %d%n", nodeId, currentTerm);
                                sendHeartbeats();
                            }
                        }
                    }
                } catch (Exception e) {
                    System.out.printf("Process %d failed to contact Process %d: %s%n", nodeId, peerId, e.getMessage());
                }
            });
        }
    }

    public void sendHeartbeats() {
        while (isLeader) {
            for (int peer : peers) {
                final int peerId = peer;
                CompletableFuture.runAsync(() -> {
                    try {
                        RaftNodeGrpc.RaftNodeBlockingStub stub = createStub(peerId);
                        AppendEntriesRequest request = AppendEntriesRequest.newBuilder()
                                .setTerm(currentTerm)
                                .setLeaderId(nodeId)
                                .build();

                        System.out.printf("Process %d sends AppendEntries to Process %d%n", nodeId, peerId);
                        stub.appendEntries(request);
                    } catch (Exception e) {
                        System.out.printf("Process %d failed to contact Process %d: %s%n", nodeId, peerId, e.getMessage());
                    }
                });
            }
            try {
                Thread.sleep(100); // Heartbeat interval
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    private RaftNodeGrpc.RaftNodeBlockingStub createStub(int peerId) {
        return RaftNodeGrpc.newBlockingStub(io.grpc.ManagedChannelBuilder
                .forAddress("localhost", 5000 + peerId)
                .usePlaintext()
                .build());
    }

    public void run() {
        scheduler.scheduleAtFixedRate(() -> {
            if (state.equals("Follower") && System.currentTimeMillis() - lastHeartbeat > timeout * 1000) {
                System.out.printf("Process %d transitioning to Candidate%n", nodeId);
                state = "Candidate";
                startElection();
            }
        }, 0, 100, TimeUnit.MILLISECONDS);
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        int nodeId = Integer.parseInt(args[0]);
        List<Integer> peers = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));
        peers.remove(Integer.valueOf(nodeId));

        Node node = new Node(nodeId, peers);

        Server server = ServerBuilder.forPort(5000 + nodeId)
                .addService(node)
                .build()
                .start();

        System.out.printf("Process %d started, listening on port %d%n", nodeId, 5000 + nodeId);
        node.run();
        server.awaitTermination();
    }
}
