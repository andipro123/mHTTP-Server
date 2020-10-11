from time import sleep
import socket
import sys
import threading
import os
import pathlib
from response import generateResponse
from utils.mediaTypes import mediaTypes
from utils.entityHeaders import entityHeaders
from logger import Logger
import parsers
import signal
sys.path.append(os.path.abspath(os.path.join('methods')))
from methods.get import parse_GET_Request
from methods.head import parse_HEAD_Request
from methods.delete import parse_DELETE_Request
from methods.post import parse_POST_Request
from methods.put import parse_PUT_Request



# Ideally get this from the config file
documentRoot = str(pathlib.Path().absolute()) + "/assets"
print(documentRoot)
method = ""


def process(data):
    try:
        global method
        headers = [i for i in data.split('\n')]
        tokens = headers[0].split(' ')
        method = tokens[0]
        if (method == 'GET'):
            return parse_GET_Request(headers)
        elif (method == 'POST'):
            return parse_POST_Request(headers)
        elif (method == 'PUT'):
            return parse_PUT_Request(headers)
        elif (method == 'HEAD'):
            return parse_HEAD_Request(headers)
        elif (method == 'DELETE'):
            return parse_DELETE_Request(headers)
    except:
        error = sys.exc_info()[0]
        print(error.with_traceback())
        return generateResponse(0, 400)


def getConnection(data):
    headers = data.split('\n')
    for i in headers[1:]:
        try:
            headerField = i[:i.index(':')]
            if (headerField == "Connection"):
                return i[i.index(':') + 2:len(i) - 1]
        except:
            pass


# Runs a thread that accepts connections on the same socket and closes the TCP connection when socket times out
def accept_client(clientsocket, client_addr):
    # print('Started the Thread')
    clientsocket.settimeout(10)
    port = list(client_addr)[1]
    # print("Served from port ", port)
    while 1:
        try:
            data = clientsocket.recv(5000)
            if (not data):
                break
            data = data.decode('utf-8')
            method = data.split('\n')[0].split(' ')[0]
            if(method == "GET" or method == "HEAD"):
                res, resource = process(data)
            else:
                res = process(data)
            clientsocket.send(res.encode('utf-8'))
            if('gzip' in res):
                clientsocket.send(
                    ('H4sIAAAAAAAA/wvJyCxWAKJEhfSqzAKF1Lzk/JTMvHQAX+v29BcAAAA=').encode('utf-8'))
            if (method == 'GET'):
                try:
                    if(len(resource)):
                        clientsocket.send(resource)
                except e:
                    print(e)
                    pass
            conntype = getConnection(data)
            if (conntype == "close"):
                clientsocket.close()
                break
        except socket.timeout:
            # print('Closing connection')
            clientsocket.close()
            break
    # print('Ended the Thread')
    return


def stopserver(signal, frame):
    s.close()
    sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, stopserver)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(sys.argv[1])))
    s.listen(90)
    print("Listening on port {}".format(sys.argv[1]))
    while 1:
        clientsocket, client_addr = s.accept()
        threading.Thread(target=accept_client,args=(clientsocket,client_addr,)).start()