import grpc
import raft_pb2
import raft_pb2_grpc


def send_client_request(node_id, operation):
    # Connect to any node (assuming node_id is passed as the argument)
    with grpc.insecure_channel(f'localhost:500{node_id}') as channel:
        stub = raft_pb2_grpc.RaftNodeStub(channel)

        # Create the ExecuteOperationRequest
        request = raft_pb2.ExecuteOperationRequest(operation=operation)

        # Send the request and get the response
        response = stub.ExecuteOperation(request)

        if response.success:
            print(f"Client: Operation '{operation}' successfully added to log.")
        else:
            print(f"Client: Failed to add operation '{operation}'.")


if __name__ == "__main__":
    node_id = int(input("Enter the node ID you want to connect to: "))
    operation = input("Enter the operation to send: ")

    send_client_request(node_id, operation)
