import socket,sys
import threading
import os

#Ideally get this from the config file
documentRoot = '/home/anup08/Desktop/CNProj'

def parse_GET_Request(headers):
    # TODO
    # Implement Conditional Get
    # Implement Range Header
    # MIME Encoding response 
    for i in headers[1:]:
        try:
            headerField = i[:i.index(':')] 
            params[headerField] = i[i.index(':') + 2 : len(i) - 1]
        except :
            pass

    # print(params)
    # Return 406 on not getting file with desired accept

    path = headers[0].split(' ')[1]
    path = documentRoot + path
    try:
        if(path == "/"):
            path = 'index.html'
        f = open(path,"r")
        print("OK")
        return "200" #Proper data encoding and sending as a HTTP response
    except FileNotFoundError:
        print("NOT OK")
        return "404" #Change to proper HTTP response


def parse_POST_Request(headers):
    pass
def parse_PUT_Request(headers):
    pass
def parse_HEAD_Request(headers):
    pass
def parse_DELETE_Request(headers):
    pass

def process(data):
    try:
        headers = [i for i in data.split('\n')]
        tokens = headers[0].split(' ')
        method = tokens[0]
        print(method)
        
        if(method == 'GET'):
            parse_GET_Request(headers)
        elif (method == 'POST'):
            parse_POST_Request(headers)
        # elif (method == 'PUT'):
        #     parse_PUT_Request(headers)
        # elif (method == 'HEAD'):
        #     parse_HEAD_Request(headers)
        # elif (method == 'DELETE'):
        #     parse_DELETE_Request(headers)

    except:
        print("Return 400 Bad request")
        return "400"






if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',int(sys.argv[1])))
    s.listen(90)

    print("Listening on port {}".format(sys.argv[1]))
    # TODO
    # Implement with multithreading 
    while 1:
        clientsocket, clientaddr = s.accept()
        # threading.Thread()
        try:
            data = clientsocket.recv(1024).decode('utf-8')
            print(data)
            process(data)
            if('\r\n\r\n' in data):
                break
        except e :
            print(e)
        finally:
            clientsocket.close()

