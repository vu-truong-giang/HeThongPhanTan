import grpc
import student_pb2 , student_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')

    stub = student_pb2_grpc.StudentServiceStub(channel)

    request = student_pb2.studentRequest(age = 20)
    response = stub.getStudent(request)
    for student in response:
        print("Student ID:", student.id)
        print("Student Name:", student.name)
        print("Student Age:", student.age)  
if __name__ == '__main__':
    run()