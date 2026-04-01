import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import grpc
import sum_pb2_grpc , sum_pb2

def run():
    channel = grpc.insecure_channel('localhost:50051')
    
    stubSum = sum_pb2_grpc.sumServiceStub(channel)

    sum_request = sum_pb2.sumRequest(a=5, b=3)
    sum_response = stubSum.Add(sum_request)

    print("Sum Result:", sum_response.result)

if __name__ == '__main__':
    run()