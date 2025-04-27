import requests
from bs4 import BeautifulSoup
from collections import defaultdict
base_url = 'https://quotes.toscrape.com'
import random
import math
import re

# 11
url = 'http://olympus.realpython.org/profiles'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a'):
    print(url + link.get('href'))

# 12
authors = defaultdict(int)

page = 1
while True:
    response = requests.get(f'{base_url}/page/{page}/')
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')
    if not quotes:
        break

    for quote in quotes:
        author = quote.find('small', class_='author').text
        authors[author] += 1

    page += 1

sorted_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
for author, count in sorted_authors:
    print(f"{author}: {count} цитат")

# 13
all_quotes = []

page = 1
while True:
    response = requests.get(f'{base_url}/page/{page}/')
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')
    if not quotes:
        break

    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        all_quotes.append(f"{text} — {author}")

    page += 1

for quote in random.sample(all_quotes, min(5, len(all_quotes))):
    print(quote)

# 14
def get_quotes_by_tags(tags):
    base_url = 'https://quotes.toscrape.com'
    tags = [tag.lower() for tag in tags]
    found_quotes = []

    page = 1
    while True:
        response = requests.get(f'{base_url}/page/{page}/')
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        if not quotes:
            break

        for quote in quotes:
            quote_tags = [tag.text.lower() for tag in quote.find_all('a', class_='tag')]
            if any(tag in quote_tags for tag in tags):
                text = quote.find('span', class_='text').text
                author = quote.find('small', class_='author').text
                found_quotes.append(f"{text} — {author} (Теги: {', '.join(quote_tags)})")

        page += 1

    return found_quotes


user_tags = input("Введите теги через запятую: ").split(',')
quotes = get_quotes_by_tags([tag.strip() for tag in user_tags])

if quotes:
    for quote in quotes:
        print(quote)
else:
    print("Цитат с указанными тегами не найдено.")