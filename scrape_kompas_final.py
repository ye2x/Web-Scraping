import requests
from bs4 import BeautifulSoup

headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
url = 'https://indeks.kompas.com/?site=all&date=2023-02-05'
link = []

for i in range (2):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    next_page = soup.select_one(".paging__link.paging__link--next[rel='next']")

    for headline in soup.select("div.article__list"):
        href = headline.find('a').get('href')
        link.append(href)

    if next_page:
        url = next_page["href"]
    else:
        break

data = []
for url in link:
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    print(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', class_="read__title").text
    time = soup.find('div', class_='read__time').text
    time = time.replace("Kompas.com - ", "").strip()
    date, hour = time.split(", ")
    author = soup.find('div', id='penulis').text if soup.find('div', id='penulis') else "Tidak ada data"
    img = soup.find('div', class_='photo__wrap')
    image= img.find('img').get('src')
    all_text = soup.select_one("div.read__content").text

    data.append((title, date, time, author,image, url, all_text))

import pandas as pd
df_scraped = pd.DataFrame(data, columns= ['Title','Date', 'Time', 'Author', 'Image', 'URL', 'News'])
df_scraped.to_excel('final_hasil_scraping.xlsx', index=False)