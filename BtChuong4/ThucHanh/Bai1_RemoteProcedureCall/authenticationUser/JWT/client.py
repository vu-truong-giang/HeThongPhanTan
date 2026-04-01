import os 
import sys 

import grpc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import student_pb2 , student_pb2_grpc
import jwt
import datetime
def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = student_pb2_grpc.StudentServiceStub(channel)

    # tạo token
    token = jwt.encode(
        {
            'username': 'test_user',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
        },
        'my_secret_key',
        algorithm = 'HS256'
    )

    # gửi request kèm metadata
    try:
        response = stub.getScore(
            student_pb2.ScoreRequest(id=1),
            metadata=[("authorization", token)]
        )
        print("Student Score:", response.score)
    except grpc.RpcError as e:
        print("Error:")
        print("Code:", e.code())
        print("Details:", e.details())
if __name__ == '__main__':
    run()