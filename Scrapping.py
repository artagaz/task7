import requests
from bs4 import BeautifulSoup
from collections import defaultdict
base_url = 'https://quotes.toscrape.com'
import random
import math

# 11
# url = 'http://olympus.realpython.org/profiles'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
#
# for link in soup.find_all('a'):
#     print(url + link.get('href'))

# 12
# authors = defaultdict(int)
#
# page = 1
# while True:
#     response = requests.get(f'{base_url}/page/{page}/')
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     quotes = soup.find_all('div', class_='quote')
#     if not quotes:
#         break
#
#     for quote in quotes:
#         author = quote.find('small', class_='author').text
#         authors[author] += 1
#
#     page += 1
#
# sorted_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
# for author, count in sorted_authors:
#     print(f"{author}: {count} цитат")

# 13
# all_quotes = []
#
# page = 1
# while True:
#     response = requests.get(f'{base_url}/page/{page}/')
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     quotes = soup.find_all('div', class_='quote')
#     if not quotes:
#         break
#
#     for quote in quotes:
#         text = quote.find('span', class_='text').text
#         author = quote.find('small', class_='author').text
#         all_quotes.append(f"{text} — {author}")
#
#     page += 1
#
# for quote in random.sample(all_quotes, min(5, len(all_quotes))):
#     print(quote)

# 14
# def get_quotes_by_tags(tags):
#     base_url = 'https://quotes.toscrape.com'
#     tags = [tag.lower() for tag in tags]
#     found_quotes = []
#
#     page = 1
#     while True:
#         response = requests.get(f'{base_url}/page/{page}/')
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         quotes = soup.find_all('div', class_='quote')
#         if not quotes:
#             break
#
#         for quote in quotes:
#             quote_tags = [tag.text.lower() for tag in quote.find_all('a', class_='tag')]
#             if any(tag in quote_tags for tag in tags):
#                 text = quote.find('span', class_='text').text
#                 author = quote.find('small', class_='author').text
#                 found_quotes.append(f"{text} — {author} (Теги: {', '.join(quote_tags)})")
#
#         page += 1
#
#     return found_quotes
#
#
# user_tags = input("Введите теги через запятую: ").split(',')
# quotes = get_quotes_by_tags([tag.strip() for tag in user_tags])
#
# if quotes:
#     for quote in quotes:
#         print(quote)
# else:
#     print("Цитат с указанными тегами не найдено.")

#15
def find_closest_product(target_price):
    base_url = 'https://scrapingclub.com/exercise/list_basic'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    products = []

    page = 1
    while True:
        try:
            print(f"Обработка страницы {page}...")
            response = requests.get(f'{base_url}/?page={page}', headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)

            # Новый способ поиска карточек товаров
            items = soup.select('div.col-lg-4.col-md-6.mb-4')
            print(items)
            if not items:
                print("Товары не найдены, завершаем сбор.")
                break

            for item in items:
                try:
                    name_elem = item.select_one('h4.card-title a')
                    price_elem = item.select_one('h5')
                    desc_elem = item.select_one('p.card-text')
                    img_elem = item.select_one('img.card-img-top')

                    if not all([name_elem, price_elem, img_elem]):
                        print("Пропущен товар с отсутствующими данными")
                        continue

                    name = name_elem.text.strip()
                    price = float(price_elem.text.replace('$', '').strip())
                    description = desc_elem.text.strip() if desc_elem else "Нет описания"
                    image = img_elem['src']
                    if not image.startswith('http'):
                        image = 'https://scrapingclub.com' + image

                    diff = abs(price - target_price)
                    products.append({
                        'name': name,
                        'price': price,
                        'description': description,
                        'image': image,
                        'diff': diff
                    })
                except Exception as e:
                    print(f"Ошибка при обработке товара: {e}")
                    continue

            page += 1
            if page > 5:  # Ограничим количество страниц для теста
                break
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            break

    if not products:
        print("Не удалось найти ни одного товара.")
        return None

    products.sort(key=lambda x: (x['diff'], x['name']))
    return products[0]


try:
    user_price = float(input("Введите цену: $"))
    product = find_closest_product(user_price)

    if product:
        print("\nРезультат поиска:")
        print(f"📌 Название: {product['name']}")
        print(f"💰 Цена: ${product['price']:.2f}")
        print(f"📝 Описание: {product['description']}")
        print(f"🖼️ Изображение: {product['image']}")
    else:
        print("❌ Товары не найдены.")
except ValueError:
    print("⚠️ Ошибка: Введите числовое значение цены.")