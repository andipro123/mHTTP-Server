# from concurrent.futures import ThreadPoolExecutor
import requests
import threading
import time
import sys

# def get_url(url):
#     return requests.get(url)

success = 0
failure = 0
def send_request(url):
    global success
    global failure

    r = requests.get(url)
    if(r.status_code < 400):
        success += 1
    else:
        failure += 1
    # time.sleep(10)
    return


if __name__ == "__main__":
    n = 100
    port = int(sys.argv[1])
    print(port)

    while (n):
        client_thread = threading.Thread(target=send_request,
                                        args=['http://127.0.0.1:{}'.format(port)])
        client_thread.start()
        n = n - 1

    print("Requests made: {}\nSuccessful Requests: {}\nFailed Requests: {}\n".format(n,success,failure))
