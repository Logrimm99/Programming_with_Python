import requests

session = requests.Session()
session.headers.update({'Authorization': 'Bearer YOUR_ACCESS_TOKEN'})

response = session.get('https://api.github.com/user')
print(response.json())
