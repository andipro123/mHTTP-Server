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
while(newcookie == ''):
    # print("Making a second request with the cookie .....\n")
    r = requests.get(url, headers = {'Cookie' : cookie})

    print(r.headers)
    newcookie = r.headers['Cookies'] if 'Cookie' in r.headers.keys() else ''
    time.sleep(1)