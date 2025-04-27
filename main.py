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
STATIC_MAPS_URL = "https://static-maps.yandex.ru/1.x/"

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

def get_point_coordinates(address):
    data = geocode(address)
    try:
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return pos.replace(' ', ',')
    except:
        return None

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
        return postal_code
    except:
        return "Не удалось определить"

def get_full_address(address):
    data = geocode(address)
    try:
        full_address = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return full_address, pos
    except:
        return None, None

def get_region(city):
    data = geocode(city)
    try:
        region = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AdministrativeArea']['AdministrativeAreaName']
        return region
    except:
        return "Не удалось определить"

def save_map_image(filename, params):
    response = requests.get(STATIC_MAPS_URL, params=params)
    with open(filename, 'wb') as f:
        f.write(response.content)

def get_southernmost_city(cities):
    min_lat = 90
    southern_city = None
    for city in cities:
        data = geocode(city)
        try:
            pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            lat = float(pos.split()[1])
            if lat < min_lat:
                min_lat = lat
                southern_city = city
        except:
            continue
    return southern_city

def calculate_distance(points):
    # Упрощенный расчет расстояния (для точного нужно использовать API маршрутизации)
    return len(points) - 1  # Заглушка

# # 2
#
# # a
# yakutsk_lat, yakutsk_lon = get_coordinates("Якутск")
# magadan_lat, magadan_lon = get_coordinates("Магадан")
#
# if yakutsk_lat and magadan_lat:
#     if yakutsk_lat > magadan_lat:
#         print("Якутск находится севернее Магадана")
#     else:
#         print("Магадан находится севернее Якутска")
#
# # b
# native_city = "Кемерово"
# native_lat, native_lon = get_coordinates(native_city)
# toronto_lat, toronto_lon = get_coordinates("Торонто, Канада")
#
# if native_lat and toronto_lat:
#     if native_lat < toronto_lat:
#         print(f"{native_city} находится южнее Торонто")
#     else:
#         print(f"Торонто находится южнее {native_city}")
#
# # c
# cities = ["Хабаровск", "Уфа", "Нижний Новгород", "Калининград", native_city]
# print("\nФедеральные округа:")
# for city in cities:
#     district = get_federal_district(city)
#     print(f"{city}: {district}")
#
# # d
# kemgu_postal = get_postal_code("Красная, 6, Кемерово")
# print("\nПочтовый индекс КемГУ:", kemgu_postal)
#
#
# # 3
# print("\nИсторический музей Москвы:")
# address, coords = get_full_address("Красная площадь, 1, Москва")
# print(f"Адрес: {address}")
# print(f"Координаты: {coords}")
#
# # 4
# print("\nОбласти городов:")
# cities = ["Барнаул", "Мелеуз", "Йошкар-Ола"]
# for city in cities:
#     region = get_region(city)
#     print(f"{city}: {region}")
#
# # 5
# print("\nПочтовый индекс МУРа:")
# postal_code = get_postal_code("Петровка, 38, Москва")
# print(f"Почтовый индекс: {postal_code}")
#
# # 6
# print("\nСохранение снимка Австралии:")
# params = {
#     "ll": "133.7751,-25.2744",
#     "spn": "40,40",
#     "l": "sat",
#     "size": "650,450"
# }
# save_map_image("australia.jpg", params)
# print("Снимок сохранен в australia.jpg")

# 7
# print("\nКарта Кемерово с отметками")
# points = [
#     ("ЖД Вокзал", "Кемерово, Кемерово-Пасс."),
#     ("Кардиодиспансер", "Кемерово, Кардиоцентр"),
#     ("Красная Горка", "Кемерово, Музей-заповедник Красная Горка"),
#     ("Парк Победы", "Кемерово, Парк Победы имени Георгия Константиновича Жукова")
# ]
#
# pt_params = []
# for label, address in points:
#     coords = get_point_coordinates(address)
#     if coords:
#         pt_params.append(f"{coords},pm2rdm")
#
# params = {
#     "ll": "86.102792,55.358422",
#     "z": "13",
#     "l": "map",
#     "pt": "~".join(pt_params),
#     "size": "650,450"
# }
# save_map_image("kemerovo.jpg", params)
# print("Карта сохранена в kemerovo.jpg")

# # №8: Карта Кемеровской области с маршрутом
# print("\n№8: Карта области с маршрутом")
# route = ["Кемерово", "Ленинск-Кузнецкий", "Новокузнецк", "Шерегеш"]
# route_coords = []
# for city in route:
#     coords = get_coordinates(city)
#     if coords:
#         route_coords.append(coords)
#
# params = {
#     "l": "map",
#     "pl": "~".join(route_coords),
#     "size": "650,450"
# }
# save_map_image("kemerovo_region.jpg", params)
# print("Карта сохранена в kemerovo_region.jpg")
#
# # №9: Самый южный город
# print("\n№9: Определение самого южного города")
# input_cities = input("Введите города через запятую: ").split(',')
# cities = [city.strip() for city in input_cities if city.strip()]
# southern_city = get_southernmost_city(cities)
# print(f"Самый южный город: {southern_city}")
#
# # №10: Длина пути и карта с меткой
# print("\n№10: Длина пути и карта")
# points = [
#     "55.7558,37.6176",  # Москва
#     "59.9343,30.3351",  # СПб
#     "56.3269,44.0065"   # Нижний Новгород
# ]
#
# # Расчет средней точки
# lats = [float(p.split(',')[0]) for p in points]
# lons = [float(p.split(',')[1]) for p in points]
# mid_lat = sum(lats) / len(lats)
# mid_lon = sum(lons) / len(lons)
# mid_point = f"{mid_lon},{mid_lat}"
#
# params = {
#     "l": "map",
#     "pl": "~".join(points),
#     "pt": f"{mid_point},pm2rdm",
#     "size": "650,450"
# }
# save_map_image("route.jpg", params)
#
# distance = calculate_distance(points)
# print(f"Длина пути (условно): {distance} точек")
# print("Карта с маршрутом сохранена в route.jpg")