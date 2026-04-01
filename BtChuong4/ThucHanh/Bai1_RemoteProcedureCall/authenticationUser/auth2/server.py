import grpc
from concurrent import futures
import login_pb2, login_pb2_grpc
import jwt
import datetime

SECRET_KEY = "my_secret_key_1234567890_abcdef"

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes = 30)
        
    }
    return jwt.encode(payload , SECRET_KEY, algorithm = 'HS256')


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except:
        return None

class StudentService(login_pb2_grpc.StudentServiceServicer):
    def Login(self , request , context):
        if request.username == "admin" and request.password == "123":
            token = generate_token(request.username)
            return login_pb2.LoginResponse(token = token)
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid username or password")

    def getScore(self , request , context):
        students = [
            {"id": 1, "name": "John Doe", "score": 85},
            {"id": 2, "name": "Jane Smith", "score": 90},
        ]

        metadata = dict(context.invocation_metadata())
        token = metadata.get("authorization")

        if not token : 
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token is missing")
        username = verify_token(token)
        if not username:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        
        for s in students:
            if s["id"] == request.id:
                return login_pb2.ScoreResponse(id = request.id, name = s["name"], score = s["score"])
        context.abort(grpc.StatusCode.NOT_FOUND, "Student not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    login_pb2_grpc.add_StudentServiceServicer_to_server(StudentService(), server)
    server.add_insecure_port("[::]:50052")
    print("Server is running on port 50051...")
    server.start()
    server.wait_for_termination()
if __name__ == "__main__":
    serve()