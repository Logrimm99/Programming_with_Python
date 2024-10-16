import requests

response = requests.get('https://getsamplefiles.com/download/txt/sample-1.txt', stream=True)
for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
