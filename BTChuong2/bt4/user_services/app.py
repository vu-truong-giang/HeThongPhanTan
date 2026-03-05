from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1 , "name": "giang"},
    {"id": 2 , "name": "huy"}
]
@app.route("/")
def home():
    return "User Service Running"
@app.route('/users')
def get_users():
    return jsonify(users)

@app.route('/user/<int:id>')
def get_user(id):
    for user in users:
        if user["id"] == id:
            return jsonify(user)
    return jsonify({"error: user not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port = 5000)
