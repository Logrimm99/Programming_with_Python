import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts')# Status code
print('Status code: ', response.status_code)
print('Headers: ', response.headers) # Headers
print('Text: ', response.text)   # Body as string
print('JSON: ', response.json()) # Body as JSON
