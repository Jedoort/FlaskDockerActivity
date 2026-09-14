from crud import add_item, delete_item, get_items, init_db, login_user, register_user
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = init_db()

#FRONTEND ROUTE
@app.route("/")
def index():
  return render_template("index.html")

#AUTH ROUTES
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    data = request.get_json() or {}
    res = login_user(db, data.get("username"), data.get("password"))
    status_code = 200 if "status" in res else 401
    return jsonify(res), status_code

  return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    data = request.get_json() or {}
    res = register_user(db, data.get("username"), data.get("password"))
    return jsonify(res), 200

  return render_template("register.html")

#ITEM API ROUTES
@app.route("/items", methods=["GET"])
def read_items():
  return jsonify(get_items(db))

@app.route("/items", methods=["POST"])
def create_items():
  data = request.get_json() or {}
  return jsonify(add_item(db, data))

@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item_route(item_id):
  return jsonify(delete_item(db, item_id))

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)