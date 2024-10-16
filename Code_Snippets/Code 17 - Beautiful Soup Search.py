import requests
from bs4 import BeautifulSoup
import re

response = requests.get('https://www.wikipedia.de/')
html = response.text
soup = BeautifulSoup(html, 'lxml')
print(soup.find('a')) # Search for the first <a> tag
print(soup.findAll(class_=re.compile('wikipedia'))) # Search for all tags with a class name containing 'wikipedia'
print(soup.findAll(string=re.compile('Wikipedia'))) # Search for all tag-contents containing 'wikipedia'
