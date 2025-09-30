from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app_for_testing")  # ここは自分のアプリ名にする
location = geolocator.reverse("34.07, 132.99", language="ja")
print(location.address)