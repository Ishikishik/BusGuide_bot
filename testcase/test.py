import random
import requests
import time

# エンドポイントURL
URL = "http://localhost:5555/query"
AUTH_CODE = "VlZqP[S3v3"

# 日本のおおよその範囲
LAT_MIN, LAT_MAX = 24.0, 45.0
LON_MIN, LON_MAX = 122.0, 146.0

# 50回テスト
for i in range(50):
    lat = round(random.uniform(LAT_MIN, LAT_MAX), 3)
    lon = round(random.uniform(LON_MIN, LON_MAX), 3)
    params = {"x": lat, "y": lon, "auth": AUTH_CODE}

    try:
        response = requests.get(URL, params=params, timeout=10)
        print(f"{i+1:02d}. ({lat}, {lon}) -> {response.text}")
    except Exception as e:
        print(f"{i+1:02d}. ({lat}, {lon}) -> ERROR: {e}")

    # API負荷軽減のため少し待機
    time.sleep(1)
