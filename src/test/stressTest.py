import requests
import threading
import time
import sys
import random
success = 0
failure = 0
lock = threading.Lock()
# methods = {1: 'get'}
def send_request(url,n):
    global success
    global failure
    # print('Client ',n)
    try:
        choice = random.randint(1,5)
        if(choice == 1):
            r = requests.get(url)   
            print('GET HTTP/1.1 ',r.status_code)

        elif(choice == 2):
            r = requests.head(url)
            print('HEAD HTTP/1.1 ',r.status_code)

        elif(choice == 3):
            data = {
                'foo' : 'bar'
            }
            r = requests.post(url,data)
            print('POST HTTP/1.1 ',r.status_code)

        elif(choice == 4):
            data = {
                'bar' : 'foo'
            }
            r = requests.put(url,data)
            print('PUT HTTP/1.1 ',r.status_code)

        else:
            r = requests.delete(url + '/random.html')
            print('DELETE HTTP/1.1 ',r.status_code)
        if(r.status_code):
            success += 1
        else:
            failure += 1
    except :
        pass
    return


if __name__ == "__main__":
    n = int(sys.argv[2])
    port = int(sys.argv[1])
    threadArray = []
    url = 'http://127.0.0.1:{}'.format(port)
    while (n):
        client_thread = threading.Thread(target=send_request,
                                        args=[url,n])

        # client_thread = threading.Thread(target=send_request,
        #                                 args=['http://34.237.242.80:5000/',n])
                                        
        client_thread.start()
        threadArray.append(client_thread)
        n = n - 1
        # client_thread.join()
    for i in threadArray:
        i.join()
    
    print(f'Successful Requests:{success}\nFailed Requests: {failure}')