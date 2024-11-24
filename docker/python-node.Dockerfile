# Use Python 3.10 as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the Python source code from your local project
COPY ../python-node/ ./

# Install necessary dependencies
RUN pip install grpcio grpcio-tools protobuf 

# Expose port 50051 for gRPC communication
EXPOSE 50051

# Run the Python Raft node script
CMD ["python", "src/node.py"]
