import requests
from requests.auth import HTTPBasicAuth

response_password = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('username', 'password')) # Get request with password authentication
print(response_password.json())

headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'} # Header for the authentication using a token
response_token = requests.get('https://api.github.com/user', headers=headers) # Get request with token authentication
print(response_token.json())
