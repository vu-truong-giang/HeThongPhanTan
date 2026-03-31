import grpc

import ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.sum_pb2_grpc as sum_pb2_grpc , ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.sum_pb2 as sum_pb2
import ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.student_pb2 as student_pb2
import ThucHanh.Bai1_RemoteProcedureCall.unaryRPC.student_pb2_grpc as student_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    
    stub = student_pb2_grpc.studentServiceStub(channel)
    stubSum = sum_pb2_grpc.sumServiceStub(channel)

    request = student_pb2.studentRequest(id=1)
    response = stub.getStudent(request)

  
    sum_request = sum_pb2.sumRequest(a=5, b=3)
    sum_response = stubSum.Add(sum_request)

    print("Student Name:", response.name)
    print("Student Age:", response.age)
    print("Sum Result:", sum_response.result)

if __name__ == '__main__':
    run()