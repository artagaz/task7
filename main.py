# 1
# a https://static-maps.yandex.ru/1.x/?ll=86.093537%2C55.350931&z=17&&size=450,450&l=map
# b https://static-maps.yandex.ru/1.x/?ll=86.134981%2C55.334086&z=17&&size=450,450&l=map
# c https://static-maps.yandex.ru/1.x/?azimuth=5.497787143782138&ll=86.949773%2C55.003320&z=15&l=map
# d https://static-maps.yandex.ru/1.x/?ll=2.2945,48.8584&spn=0.005,0.005&l=sat
# e https://static-maps.yandex.ru/1.x/?ll=158.8300,53.2557&spn=0.1,0.1&l=sat
# f https://static-maps.yandex.ru/1.x/?ll=107.6736,53.7212&spn=2,2&l=sat
# g https://static-maps.yandex.ru/1.x/?ll=63.3083,45.9646&spn=0.1,0.1&l=sat

# 2
import requests

API_KEY = "c1f9c6cc-3d3a-4be7-943c-7379bb211fc1"
BASE_URL = "https://geocode-maps.yandex.ru/1.x/"

def geocode(address):
    params = {
        "apikey": API_KEY,
        "format": "json",
        "geocode": address
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def get_coordinates(city):
    data = geocode(city)
    pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    longitude, latitude = pos.split()
    return float(latitude), float(longitude)

def get_federal_district(city):
    data = geocode(city)
    try:
        district = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        return district
    except:
        return "Не удалось определить"

def get_postal_code(address):
    data = geocode(address)
    try:
        postal_code = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        print(postal_code)
        return postal_code
    except:
        return "Не удалось определить"

# a
yakutsk_lat, yakutsk_lon = get_coordinates("Якутск")
magadan_lat, magadan_lon = get_coordinates("Магадан")

print("\na) Координаты:")
print(f"Якутск: {yakutsk_lat}° с.ш., {yakutsk_lon}° в.д.")
print(f"Магадан: {magadan_lat}° с.ш., {magadan_lon}° в.д.")

if yakutsk_lat and magadan_lat:
    if yakutsk_lat > magadan_lat:
        print("Якутск находится севернее Магадана")
    else:
        print("Магадан находится севернее Якутска")

# b
native_city = "Кемерово"
native_lat, native_lon = get_coordinates(native_city)
toronto_lat, toronto_lon = get_coordinates("Торонто, Канада")

print("\nb) Координаты:")
print(f"{native_city}: {native_lat}° с.ш., {native_lon}° в.д.")
print(f"Торонто: {toronto_lat}° с.ш., {toronto_lon}° з.д.")

if native_lat and toronto_lat:
    if native_lat < toronto_lat:
        print(f"{native_city} находится южнее Торонто")
    else:
        print("Торонто находится южнее")

# c
cities = ["Хабаровск", "Уфа", "Нижний Новгород", "Калининград", native_city]
print("\nc) Федеральные округа:")
for city in cities:
    district = get_federal_district(city)
    print(f"{city}: {district}")

# d
kemgu_postal = get_postal_code("КемГУ, Кемерово")
print("\nd) Почтовый индекс КемГУ:", kemgu_postal)