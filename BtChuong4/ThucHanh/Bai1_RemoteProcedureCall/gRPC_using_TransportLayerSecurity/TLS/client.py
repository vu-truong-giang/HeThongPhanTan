import os 
import sys
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))

import grpc
import sum_pb2 , sum_pb2_grpc

def run():
    #đọc file cert
    with open(os.path.join(BASE_DIR, "ca.crt"), "rb") as f:
        trusted_certs = f.read()
    
    # Tạo ssl credentials 
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    channel = grpc.secure_channel('Localhost:50051', credentials)
    stub = sum_pb2_grpc.SumServiceStub(channel)

    a = 5
    b = 10
    response = stub.getSum(sum_pb2.sumRequest(a=a, b=b))
    print("Sum of", a, "and", b, "is", response.result)
if __name__ == '__main__':
    run();