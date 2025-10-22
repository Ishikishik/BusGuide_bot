#coordinates2guid
import os
from dotenv import load_dotenv
import google.generativeai as genai
from geopy.geocoders import Nominatim
#to_romaji
import pykakasi
#insert_commas
from tinysegmenter import TinySegmenter
#jcc
import json


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
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    prompt = f"""
あなたは観光案内役です。
以下の住所情報から、日本語で観光案内を1文だけ生成してください。
出力形式は **必ずこの形** に従ってください：

「現在地は〇〇、名物は〇〇でございます。」

・15文字程度
・余計な説明や前置き（承知しました等）は不要
・上記形式以外の文章は出力しないこと

住所情報: {address}
"""

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=30,
            temperature=0.2,
        ),
    )

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

#lsiのために句点を増やす
segmenter = TinySegmenter()
def insert_commas(text: str) -> str:
    text = text.replace(",", "/")
    text = text.replace(",", "/")
    words = segmenter.tokenize(text)
    new_text = "/"
    for w in words:
        new_text += w
        # 「は」「が」「でございます」などの後に句読点を挿入
        if w in ["は", "が", "です", "でございます"]:
            new_text += "/"
    return new_text


#以下jccに関するコード群#################################################
# ---- 数字の読みをローマ字で ----
num_read = {
    "0": "maru",
    "1": "ichi",
    "2": "ni",
    "3": "san",
    "4": "yon",
    "5": "go",
    "6": "roku",
    "7": "nana",
    "8": "hachi",
    "9": "kyuu",
}

def num_to_reading(num_str: str) -> str:
    """JCC番号をローマ字読みへ変換"""
    return " ".join(num_read[d] for d in str(num_str))

# ---- pykakasi でローマ字変換 ----
kks = pykakasi.kakasi()
def to_romaji(text: str) -> str:
    result = kks.convert(text)
    return "".join([item['hepburn'] for item in result])

# ---- 住所取得 ----
def get_city_pref(lat, lon):
    geolocator = Nominatim(user_agent="my_app_for_testing")
    location = geolocator.reverse((lat, lon), language="ja")
    
    if not location:
        return None, None

    addr = location.raw.get("address", {})

    prefecture = addr.get("state") or addr.get("region") or addr.get("province") or addr.get("county")
    city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("municipality") or addr.get("county")
    
    if not prefecture:
        parts = [p.strip() for p in location.address.split(",")]
        if len(parts) >= 3:
            prefecture = parts[-3]
    
    return prefecture, city

# ---- JCC関連 ----
def load_jcc(json_path=None):
    if json_path is None:
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, "jcc.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_jcc_from_city(prefecture: str, city: str, jcc_dict: dict) -> str:
    """
    都道府県と市区町村からJCCコードを取得し、ローマ字で返す
    """
    code = None
    if prefecture in jcc_dict and city in jcc_dict[prefecture]:
        code = jcc_dict[prefecture][city]
    else:
        # 接尾辞を除去して再検索
        suffixes = ["市", "区", "町", "村"]
        if city and city[-1] in suffixes:
            city_trimmed = city[:-1]
            if prefecture in jcc_dict and city_trimmed in jcc_dict[prefecture]:
                code = jcc_dict[prefecture][city_trimmed]

    if code is None:
        return f"mitoroku: {prefecture} {city}"

    pref_en = to_romaji(prefecture)
    city_en = to_romaji(city)
    code_read = num_to_reading(str(code))
    return f"genzaichi/ {pref_en} {city_en} /jcc nanbaa/ {code_read}"

def returnjcc(lat, lon):
    prefecture, city = get_city_pref(lat, lon)
    if not prefecture or not city:
        return "住所取得失敗"

    jcc_dict = load_jcc()
    return extract_jcc_from_city(prefecture, city, jcc_dict)