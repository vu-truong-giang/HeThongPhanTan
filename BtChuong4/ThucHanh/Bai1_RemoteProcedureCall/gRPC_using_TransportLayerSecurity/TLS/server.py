import os 
import sys
BASE_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, '..')))


import grpc
from concurrent import futures
import sum_pb2 , sum_pb2_grpc

class SumService(sum_pb2_grpc.SumServiceServicer):
    def getSum(self , request , context):
        print("Received request to calculate sum of", request.a, "and", request.b)
        result = request.a + request.b
        return sum_pb2.sumResponse(result=result)
    
def serve():
    
    #đọc file cert  
    with open(os.path.join(BASE_DIR,"server.key"), "rb") as f:
        private_key = f.read()
    with open(os.path.join(BASE_DIR,"server.crt"), "rb") as f:
        certificate_chain = f.read()
    
    #tạo ssl credential
    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)]
    )

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sum_pb2_grpc.add_SumServiceServicer_to_server(SumService(), server)

    #add secure port 
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()
if __name__ == '__main__':
    serve()