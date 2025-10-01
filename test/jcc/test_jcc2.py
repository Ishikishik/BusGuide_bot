import os
import json
from geopy.geocoders import Nominatim
import pykakasi

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
    return f"genzaichi {pref_en} {city_en} jcc nanbaa {code_read}"

def returnjcc(lat, lon):
    prefecture, city = get_city_pref(lat, lon)
    if not prefecture or not city:
        return "住所取得失敗"

    jcc_dict = load_jcc()
    return extract_jcc_from_city(prefecture, city, jcc_dict)

# ---- テスト ----
if __name__ == "__main__":
    print(returnjcc(35.676,139.809))  # 渋谷付近



"""
てすとけーす(笑)
日立 36.594,140.662
中央区35.676,139.809
苫小牧 42.634,141.606
横浜市35.438,139.639
川崎市35.524,139.707
相模原市35.572,139.368






"""
