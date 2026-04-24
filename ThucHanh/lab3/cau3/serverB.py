from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    print("Server B received a request")
    return "Server B"

app.run(port=5002)