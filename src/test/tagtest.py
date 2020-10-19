import requests
import sys
port = sys.argv[1]
url = "http://localhost:{}/test.pdf".format(port)

print("Getting metadata about the resource.")
r = requests.head(url)
etag = r.headers['E-Tag']

print("Checking if the resource is modified.")
r = requests.get(url, headers = {'If-None-Match' : etag})
print(r.status_code)