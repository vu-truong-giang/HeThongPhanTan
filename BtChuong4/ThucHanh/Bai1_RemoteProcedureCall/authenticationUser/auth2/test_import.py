#!/usr/bin/env python
import traceback
import sys

try:
    print("Python version:", sys.version)
    print("Python path:", sys.executable)
    import login_pb2
    print("Import success!")
    print("ScoreRequest:", dir(login_pb2.ScoreRequest))
except Exception as e:
    print("Error:", str(e))
    traceback.print_exc()
