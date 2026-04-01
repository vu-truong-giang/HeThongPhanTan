
import grpc
from concurrent import futures
import sum_pb2_grpc , sum_pb2
###implement the server

class sumService(sum_pb2_grpc.sumServiceServicer):
    def Add(self , request , context):
        print("Received request to calculate sum of:", request.a , "and" , request.b)

        result = request.a + request.b
        return sum_pb2.sumResponse(result = result)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sum_pb2_grpc.add_sumServiceServicer_to_server(sumService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    