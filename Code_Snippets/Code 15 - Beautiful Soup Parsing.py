import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.wikipedia.de/')
html = response.text

soup = BeautifulSoup(html, 'lxml')
print(soup)
