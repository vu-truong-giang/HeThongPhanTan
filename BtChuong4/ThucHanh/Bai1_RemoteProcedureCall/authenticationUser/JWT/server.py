import os
import sys

import grpc
from concurrent import futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import student_pb2 , student_pb2_grpc

import jwt
import datetime

SECRET_KEY = 'my_secret_key'

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=["HS256"])
        return payload["username"]
    except:
        return None

class StudentService(student_pb2_grpc.StudentServiceServicer):
    def getScore(self, request, context):

        students = [
            {"id": 1, "name": "John Doe", "score": 85},
            {"id": 2, "name": "Jane Smith", "score": 90},
            {"id": 3, "name": "Alice Johnson", "score": 78},
            {"id": 4, "name": "Bob Brown", "score": 92}
        ]

        #lấy metadata
        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")

        if not token: 
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "token is missing")
        
        username = verify_token(token)

        if not username:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "invalid token")

        for s in students:
            if s["id"] == request.id:
                return student_pb2.ScoreResponse(
                    id = request.id,
                    name = s["name"],
                    score = s["score"]
                )

        context.abort(grpc.StatusCode.NOT_FOUND, "Student not found")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
