#coordinates2guid
import os
from dotenv import load_dotenv
import google.generativeai as genai
from geopy.geocoders import Nominatim
#to_romaji
import pykakasi

def coordinates2guid(lat, lon): #入力:緯度経度、出力:地名とガイド
    # Nominatimで逆ジオコーディング
    geolocator = Nominatim(user_agent="my_app_for_testing")
    location = geolocator.reverse((lat, lon), language="ja")
    address = location.address
    # .env をロードして Gemini API キーを取得
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    # Gemini モデルを設定
    model = genai.GenerativeModel("gemini-flash-latest")
    prompt = f"{address} の都市名と名物を25文字程度で現在地は何々、名物は何々でございますの口調で教えてください"
    response = model.generate_content(prompt)

    return response.text
# 使用例
#print(coordinates2guid(34.07, 132.99))


def to_romaji(text: str) -> str: #入力:漢字およびひらがな、出力:ローマ字
    kakasi = pykakasi.kakasi()

    # setModeを使わず、直接convertして "hepburn" を使う
    result = kakasi.convert(text)

    return "".join([item["hepburn"] for item in result])
#使用例
#print(to_romaji("愛媛県西条市"))

