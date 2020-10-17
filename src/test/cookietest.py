import requests




port = 5001
url = 'http://localhost:{}/cart'.format(port)
r = requests.get(url)

print(r.headers)
cookie = (r.headers['Set-Cookie'])

r = requests.get(url, {'cookie' : cookie})

print(r.headers)