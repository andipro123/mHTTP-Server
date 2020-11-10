import requests
import sys
import time

newcookie = ''
port = sys.argv[1]
url = 'http://localhost:{}/login'.format(port)
print("Making a first time request.....\n")
r = requests.get(url)
cookie = (r.headers['Set-Cookie'])
print("Recieved cookie from server:\n{}\n".format(cookie))
r = requests.get(url, headers = {'Cookie' : cookie})
print("Making a second request with the cookie .....\n")
print(r.status_code)