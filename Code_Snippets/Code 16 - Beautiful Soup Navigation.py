import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.wikipedia.de/')
html = response.text
soup = BeautifulSoup(html, 'lxml')
print(soup)
print('\n\nsoup.body: ', soup.body)
print('\n\nsoup.body.a: ', soup.body.a)
print('\n\nsoup.body.contents: ', soup.body.contents)
print('\n\nsoup.body.parent: ', soup.body.parent)
print('\n\nsoup.body.next_sibling: ', soup.body.next_sibling)
print('\n\nsoup.body.next_element: ', soup.body.next_element)
