
"""
/server/library/で使ってるlibrary
#coordinates2guid
import os
from dotenv import load_dotenv
import google.generativeai as genai
from geopy.geocoders import Nominatim

#to_romaji
import pykakasi
"""
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from library import coordinates2guid, to_romaji, returnjcc, insert_commas

app = Flask(__name__)
load_dotenv()
valid_auth_code = os.getenv("VALID_AUTH_CODE")

@app.route("/")
def index():
    return "<h1>Flask サーバー起動成功！</h1>"

@app.route("/query", methods=["GET"])
def query():
    x = request.args.get("x")
    y = request.args.get("y")
    auth = request.args.get("auth")
    mode = request.args.get("mode", "nomal")  # デフォルトはローマ字
    jcc = request.args.get("jcc", "no")

    if auth != valid_auth_code:
        return "Invalid authentication", 403

    # jcc = yes の場合は JCC モード
    if jcc == "yes":
        return returnjcc(x, y)

    # 通常モード
    if mode == "roma":
        return to_romaji(insert_commas(coordinates2guid(x, y)))
    elif mode == "nomal":
        return coordinates2guid(x, y)
    else:
        return "Invalid mode", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)