from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from crud import init_db, get_items, add_item, delete_item, login_user, register_user

app = Flask(__name__)
CORS(app)
db = init_db()

@app.route('/items', methods=['GET'])
def read_items():
    return jsonify(get_items(db))

@app.route('/items', methods=['POST'])
def create_items():
    data = request.get_json()
    return jsonify(add_item(db, data))

@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item_route(item_id):
    return jsonify(delete_item(db, item_id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return jsonify(register_user(db, data['username'], data['password']))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    res = login_user(db, data['username'], data['password'])
    status_code = 200 if "status" in res else 401
    return jsonify(res), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

