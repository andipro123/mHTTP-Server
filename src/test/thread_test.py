import requests
import threading
import time
import sys

success = 0
failure = 0
lock = threading.Lock()
def send_request(url,n):
    global success
    global failure
    print('Client ',n)
    try:
        r = requests.get(url)   
        print(r.status_code)
        if(r.status_code == 200):
            success += 1
        else:
            failure += 1
    except:
        pass
    return


if __name__ == "__main__":
    n = int(sys.argv[2])
    port = int(sys.argv[1])
    print(port)
    threadArray = []
    while (n):
        client_thread = threading.Thread(target=send_request,
                                        args=['http://127.0.0.1:{}'.format(port),n])

        # client_thread = threading.Thread(target=send_request,
        #                                 args=['http://34.237.242.80:5000/',n])
                                        
        client_thread.start()
        threadArray.append(client_thread)
        n = n - 1
    
    for i in threadArray:
        i.join()
    
    print(f'Successful Requests:{success}\nFailed Requests: {failure}')