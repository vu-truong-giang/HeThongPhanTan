import grpc
from concurrent import futures
import concat_pb2
import concat_pb2_grpc

class StringService(concat_pb2_grpc.StringServiceServicer):
    def Concat(self, request, context):
        result = request.s1 + request.s2
        return concat_pb2.ConcatResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    concat_pb2_grpc.add_StringServiceServicer_to_server(StringService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()