from geopy.geocoders import Nominatim


def get_city_pref(lat, lon):
    """
    緯度・経度から都道府県と市区町村を取得する関数
    Nominatimのaddressフィールドをもとに複数の候補から取得する
    """
    geolocator = Nominatim(user_agent="my_app_for_testing")
    location = geolocator.reverse((lat, lon), language="ja")
    
    if not location:
        return None, None

    addr = location.raw.get("address", {})

    # 都道府県を取得（state, region, province の順にチェック）
    prefecture = addr.get("state") or addr.get("region") or addr.get("province") or addr.get("county")
    
    # 市区町村を取得（city, town, village, municipality, county の順にチェック）
    city = (
        addr.get("city") or
        addr.get("town") or
        addr.get("village") or
        addr.get("municipality") or
        addr.get("county")
    )
    
    # 都道府県が None の場合、住所文字列から推定する
    if not prefecture:
        parts = [p.strip() for p in location.address.split(",")]
        if len(parts) >= 3:
            prefecture = parts[-3]  # 郵便番号の前くらいに都道府県があることが多い
    
    return prefecture, city


# テスト
pref, city = get_city_pref(36.594, 140.661)
print(pref, city)  # -> "千葉県" "船橋市" など
