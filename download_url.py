import requests

url = input('请输入URL:')

try:
    r = requests.get(url)
    r.raise_for_status()
    with open(url.split('/')[-1], 'wb') as f:
        f.write(r.content)
except Exception as e:
    print(e)

