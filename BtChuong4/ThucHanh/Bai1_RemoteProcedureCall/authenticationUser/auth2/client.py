import grpc
from concurrent import futures
import login_pb2, login_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50052")
    stub = login_pb2_grpc.StudentServiceStub(channel)

    try:
        login_res = stub.Login(
            login_pb2.LoginRequest(username = "admin", password = "123")
        )
        print("Login successful! Token:", login_res.token)

        response = stub.getScore(
            login_pb2.ScoreRequest(id = 1),
            metadata = [("authorization", login_res.token)]
        )

        print(f"Student: {response.name}, Score: {response.score}")
    except grpc.RpcError as e:
        print("Error:", e.code(), e.details())
if __name__ == "__main__":
    run()