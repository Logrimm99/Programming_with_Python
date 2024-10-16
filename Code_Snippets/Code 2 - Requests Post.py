import requests

payload = {'title': 'postTitle', 'body': 'postBody', 'userId': 1}
response = requests.post('https://jsonplaceholder.typicode.com/posts', json=payload)
print(response.json())
