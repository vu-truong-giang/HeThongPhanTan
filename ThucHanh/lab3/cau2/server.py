import grpc
from concurrent import futures
import threading
import active_pb2
import active_pb2_grpc 

class StateService(active_pb2_grpc.StateServiceServicer):
    def __init__(self):
        self.is_active = True
        self.lock = threading.Lock()

    def Deactivate(self, request, context):
        with self.lock:  # 🔒 khóa khi ghi
            self.is_active = False
            print("Server deactivated")

        return active_pb2.StateResponse(is_active=self.is_active)

    def GetState(self, request, context):
        with self.lock: # 🔒 khóa khi đọc
            current_state = self.is_active

        return active_pb2.StateResponse(is_active=current_state)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    active_pb2_grpc.add_StateServiceServicer_to_server(StateService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server running...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()