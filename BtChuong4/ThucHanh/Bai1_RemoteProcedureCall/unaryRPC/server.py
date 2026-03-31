import grpc
from concurrent import futures
import ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.student_pb2 as student_pb2 , ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.student_pb2_grpc as student_pb2_grpc
import ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.sum_pb2 as sum_pb2 , ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.sum_pb2_grpc as sum_pb2_grpc

###implement the server
class studentService(student_pb2_grpc.studentServiceServicer):
    def getStudent(self , request , context):
        print("Received request for student with id:", request.id)

        #simulator database
        return student_pb2.studentResponse(
            name = "John Doe",
            age = 20
        )
class sumService(sum_pb2_grpc.sumServiceServicer):
    def Add(self , request , context):
        print("Received request to calculate sum of:", request.a , "and" , request.b)

        result = request.a + request.b
        return sum_pb2.sumResponse(result = result)
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_pb2_grpc.add_studentServiceServicer_to_server(studentService(), server)
    sum_pb2_grpc.add_sumServiceServicer_to_server(sumService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
    