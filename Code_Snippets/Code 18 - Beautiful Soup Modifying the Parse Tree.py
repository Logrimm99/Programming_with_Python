import requests
from bs4 import BeautifulSoup
import re

response = requests.get('https://www.wikipedia.de/')
html = response.text
soup = BeautifulSoup(html, 'lxml')
wiki_occurrences = soup.findAll(string=re.compile('Wikipedia')) # Search for all tag-contents containing 'wikipedia'
for wiki_occurrence in wiki_occurrences:
    print(wiki_occurrence.parent.string)
    wiki_occurrence.parent.string = wiki_occurrence.parent.string.replace('Wikipedia', 'Wiki')

print('\n\n', soup)
