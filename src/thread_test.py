# from concurrent.futures import ThreadPoolExecutor
import requests
import threading
import time


# def get_url(url):
#     return requests.get(url)
def send_request(url):
    print(requests.get(url))
    time.sleep(10)
    return


n = 10

while (n):
    client_thread = threading.Thread(target=send_request,
                                     args=['http://127.0.0.1:12001'])
    client_thread.start()
    n = n - 1

# with ThreadPoolExecutor(max_workers=50) as pool:
#     print(list(pool.map(get_url, ['http://127.0.0.1:12001'] * 10)))
