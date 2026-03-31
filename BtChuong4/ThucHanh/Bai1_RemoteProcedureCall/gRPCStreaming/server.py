import grpc
from concurrent import futures
import student_pb2, student_pb2_grpc

class studentService(student_pb2_grpc.StudentServiceServicer):
    def getStudent(self , request , context):
        student = [
            {"id": 1, "name": "John Doe", "age": 20},
            {"id": 2, "name": "Jane Smith", "age": 22},
            {"id": 3, "name": "Alice Johnson", "age": 20},
            {"id": 4, "name": "Bob Brown", "age": 25}
        ]
        print("Received request find student has the same age:", request.age);

        for s in student: 
            if s["age"] == request.age:
                yield student_pb2.studentResponse(
                    id = s["id"],
                    name = s["name"],
                    age = s["age"]
                )
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_pb2_grpc.add_StudentServiceServicer_to_server(studentService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    serve()