import grpc
import concat_pb2
import concat_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = concat_pb2_grpc.StringServiceStub(channel)

    response = stub.Concat(concat_pb2.ConcatRequest(
        s1="$S_1",
        s2="S2_$"
    ))

    print("Result:", response.result)

if __name__ == "__main__":
    run()