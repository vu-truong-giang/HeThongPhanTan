import os
import sys
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))

import grpc
import sum_pb2 , sum_pb2_grpc

def run():
    with open(os.path.join(BASE_DIR, "client.key") , "rb") as f:
        client_key = f.read()
    with open(os.path.join(BASE_DIR, "client.crt") , "rb") as f:
        client_cert = f.read()
    with open(os.path.join(BASE_DIR, "ca.crt") , "rb") as f:
        trusted_certs = f.read()
    
    credentials = grpc.ssl_channel_credentials(
        root_certificates=trusted_certs,
        private_key=client_key,
        certificate_chain=client_cert
    )

    channel = grpc.secure_channel('Localhost:50051', credentials)
    stub = sum_pb2_grpc.SumServiceStub(channel)

    a= 5
    b= 10
    response = stub.getSum(sum_pb2.sumRequest(a=a, b=b))
    print("Sum:", response.result)
if __name__ == '__main__':
    run()