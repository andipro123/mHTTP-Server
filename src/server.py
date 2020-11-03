from time import sleep
import socket
import sys
import threading
import time
import os
import pathlib
from response import generateResponse
from utils.mediaTypes import mediaTypes
from utils.entityHeaders import entityHeaders
from logger import Logger
import parsers
import signal
sys.path.append(os.path.abspath(os.path.join('methods')))
sys.path.append(os.path.abspath(os.path.join('config')))

from methods.get import parse_GET_Request
from methods.head import parse_HEAD_Request
from methods.delete import parse_DELETE_Request
from methods.post import parse_POST_Request
# from methods.put import parse_PUT_Request
# from getconfig import getconfig
from config.config import DOCUMENT_ROOT, MAX_CONNECTIONS, PORT
documentRoot = DOCUMENT_ROOT
method = ""
logger = Logger()


def process(data, client_addr, raw=None):

    try:
        global method
        headers = [i for i in data.split('\n')]
        tokens = headers[0].split(' ')
        httpVersion = tokens[2]
        method = tokens[0]
        if (method == 'GET'):
            return parse_GET_Request(headers, client_addr)
        elif (method == 'POST'):
            return parse_POST_Request(headers, client_addr, raw)
        elif (method == 'PUT'):
            return parse_PUT_Request(headers, client_addr)
        elif (method == 'HEAD'):
            return parse_HEAD_Request(headers, client_addr)
        elif (method == 'DELETE'):
            return parse_DELETE_Request(headers, client_addr)
        else:
            logger.generateError(501)
            return generateResponse(0, 501)
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
    hostip = list(client_addr)[0]
    while 1:
        try:
            data_raw = clientsocket.recv(10485760)
            # print(data_raw)
            # print('raw', len(data_raw))

            if (not data_raw):
                break
            data = data_raw.decode('ISO-8859-1')
            # print('decoded', len(data))

            # ff = open('temp', 'w+b')
            # ff.write(data_raw)
            # print('raw: ', data)
            method = data.split('\n')[0].split(' ')[0]
            if (method == "GET" or method == "HEAD" or method == "POST"):
                res, resource = process(data, client_addr, data_raw)
            else:
                res = process(data, client_addr)
            clientsocket.send(res.encode('utf-8'))
            if (method == 'GET' or method == 'POST'):
                try:
                    if (len(resource)):
                        clientsocket.send(resource)
                except e:
                    print(e)
                    pass
            conntype = getConnection(data)
            if (conntype == "close"):
                clientsocket.close()
                break
        except socket.timeout:
            clientsocket.close()
            break
    return


def stopserver(signal, frame):
    s.close()
    sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, stopserver)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(90)
    threadArray = []
    print("Listening on port {}".format(PORT))
    while 1:
        clientsocket, client_addr = s.accept()
        t = threading.Thread(target=accept_client,
                             args=(
                                 clientsocket,
                                 client_addr,
                             ))
        t.start()
        threadArray.append(t)
        if threading.active_count() > MAX_CONNECTIONS:
            t.join()
            time.sleep(5)

        print(threading.active_count())
    for i in threadArray:
        i.join()
