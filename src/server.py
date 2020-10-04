import socket, sys
import threading
import os
from response import generateResponse 

#Ideally get this from the config file
documentRoot = '/home/anup08/Desktop/CNProj/mhttp-server/src'
resource = None
f = None
def matchAccept(headers):
    k = headers.split(',')
    # for i in k:
        # print(i)




def parse_GET_Request(headers):
    # TODO
    # Implement Conditional Get
    # Implement Range Header
<<<<<<< HEAD
    # MIME Encoding response
=======
    # MIME Encoding response 
    params = {}
>>>>>>> 4643ebb965cee9b537ae83ad9db830c989e719fe
    for i in headers[1:]:
        try:
            headerField = i[:i.index(':')]
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            pass

    # print(params)
    # Return 406 on not getting file with desired accept
    matchAccept(params['Accept'])
    path = headers[0].split(' ')[1]
    data = 0
    try:
        if (path == "/"):
            path = 'index.html'
<<<<<<< HEAD
        f = open(path, "r")
        print("OK")
        return "200"  #Proper data encoding and sending as a HTTP response
    except FileNotFoundError:
        print("NOT OK")
        return "404"  #Change to proper HTTP response
=======
        else:
            path = documentRoot + path
        global resource
        global f
        f = open(path,"r")
        resource = f.read()
        try:
            data = len(resource)
        except :
            pass
        # print("OK")
        res = generateResponse(data,200)
        return res #Proper data encoding and sending as a HTTP response
    except FileNotFoundError:
        res = generateResponse(data,404)
        return res #Change to proper HTTP response
>>>>>>> 4643ebb965cee9b537ae83ad9db830c989e719fe


def parse_POST_Request(headers):
    # TODO
    # Annotation of existing resources
    # Posting message to an existing bulleting, news board etc
    # Providing a block of data, such as the result of submitting a form, to a data-handling process
    # Extending a database through an append operation.

    # For the purpose of the project, POST methods will write the incoming data into a logs file
    for i in headers[1:]:
        try:
            headerField = i[:i.index(':')]
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            pass

    path = headers[0].split(' ')[1]
    path = documentRoot + path
    
    try:
        if (path == "/"):
            path = 'index.html'
        
        f = open('./logs/post_log.txt')



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
<<<<<<< HEAD
        print(method)

        if (method == 'GET'):
            parse_GET_Request(headers)
=======
        
        if(method == 'GET'):
            return parse_GET_Request(headers)
>>>>>>> 4643ebb965cee9b537ae83ad9db830c989e719fe
        elif (method == 'POST'):
            parse_POST_Request(headers)
        # elif (method == 'PUT'):
        #     parse_PUT_Request(headers)
        # elif (method == 'HEAD'):
        #     parse_HEAD_Request(headers)
        # elif (method == 'DELETE'):
        #     parse_DELETE_Request(headers)
        return
    except e:
        print(e)
        print("Return 400 Bad request")
        return generateResponse(0,400)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(sys.argv[1])))
    s.listen(90)

    print("Listening on port {}".format(sys.argv[1]))
    # TODO
    # Implement with multithreading
    while 1:
        clientsocket, clientaddr = s.accept()
        # threading.Thread()
        try:
<<<<<<< HEAD
            data = clientsocket.recv(1024).decode('utf-8')
            print(data)
            process(data)
            if ('\r\n\r\n' in data):
                break
=======
            while 1:
                data = clientsocket.recv(5000).decode('utf-8')
                # print(data)
                res = process(data)
                if('\r\n\r\n' in data):
                    break
            print(res)
            res = res.encode('utf-8')
            data = resource
            # clientsocket.send(res)
            # clientsocket.send(b'\n')
            # clientsocket.send(data.encode('utf-8'))
            clientsocket.send(b"HTTP/1.1 200 OK\n"
         +"Content-Type: text/html\n"
         +"\n" # Important!
         +"<html><body>Hello World</body></html>\n");
>>>>>>> 4643ebb965cee9b537ae83ad9db830c989e719fe
        except e:
            print(e)
            print("err")
        finally:
            clientsocket.close()
<<<<<<< HEAD
=======
            f.close()

>>>>>>> 4643ebb965cee9b537ae83ad9db830c989e719fe
