import requests
import sys
import time
print("Making a first time request.....")

port = sys.argv[1]
url = 'http://localhost:{}/cart'.format(port)

r = requests.get(url)
cookie = (r.headers['Set-Cookie'])
print("Recieved cookie from server:\n{}".format(cookie))

print("Making a second request with the cookie .....")
r = requests.get(url, headers = {'Cookie' : cookie})

print(r.status_code)