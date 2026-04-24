from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    print("Server A received a request")
    return "Server A"

app.run(port=5001)