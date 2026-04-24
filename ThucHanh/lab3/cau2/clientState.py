import grpc
import active_pb2
import active_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = active_pb2_grpc.StateServiceStub(channel)

response = stub.GetState(active_pb2.Empty())
print("Current state:", response.is_active)