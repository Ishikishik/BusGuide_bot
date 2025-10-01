# main/main.py または server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# テスト用認証コード
VALID_AUTH_CODE = "1234"

@app.route("/")
def index():
    return "<h1>Flask サーバー起動成功！</h1>"

@app.route("/query", methods=["GET"])
def query():
    x = request.args.get("x")
    y = request.args.get("y")
    auth = request.args.get("auth")

    if auth != "1234":
        return "Invalid authentication", 403

    # プレーンテキストで返す
    return "nihon"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
