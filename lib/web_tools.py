import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/67.0.3396.79 Safari/537.36'
}

def is_ext_network_connectable():
    try:
        r = requests.get(r"https://www.baidu.com", headers=HEADERS)
        r.raise_for_status()
        if not len(r.text)>1000:
            raise Exception('联网失败')
        return True
    except:
        return False

def get_binary_src(url, filename=None):
    if filename is None:
        filename = url.split('/')[-1]

    r = requests.get(url)
    r.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(r.content)
