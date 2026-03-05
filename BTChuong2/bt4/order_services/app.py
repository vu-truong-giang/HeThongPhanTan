
from flask import Flask , jsonify
import requests

app = Flask(__name__)

orders = [
    {"id": 1 , "user_id": 1 , "product" : "laptop"},
    {"id": 2 , "user_id": 2 , "product" : "macbook"}
]
@app.route("/")
def home():
    return "User Service Running"
@app.route('/orders')
def get_orders():
    return jsonify(orders)

@app.route('/order/<int:id>')
def get_order(id):
    for order in orders:
        if order["id"] == id:
            # Dùng request để gọi api
            user = requests.get(
                f"http://user_service:5000/user/{order['user_id']}"
            ).json()
            return jsonify({
                "order": order,
                "user" : user
            })
    return jsonify({"error: order not found"}) , 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)



