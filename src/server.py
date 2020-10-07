import socket
import sys
import threading
import os
import pathlib
from response import generateResponse
from utils.mediaTypes import mediaTypes
from logger import Logger

# Ideally get this from the config file
documentRoot = str(pathlib.Path().absolute())
# print(documentRoot)
resource = None
f = None
method = ""
logger = None


def matchAccept(headers):
    k = headers.split(',')
    par = []
    for i in k:
        par.append(i)
    return par


def parse_GET_Request(headers, method=""):
    # TODO
    # Implement Conditional Get
    # Implement Range Header
    # MIME Encoding response
    # Cache parameters

    params = {}
    for i in headers[1:]:
        try:
            headerField = i[:i.index(':')]
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            pass

    # Return 406 on not getting file with desired accept
    global logger
    par = matchAccept(params['Accept'])
    path = headers[0].split(' ')[1]
    length = 0
    try:
        if (path == "/"):
            path = 'index.html'
        else:
            path = documentRoot + path
        global resource
        global f
        f = open(path, "rb")
        resource = f.read()
        lastModified = os.path.getmtime(path)
        try:
            length = len(resource)
        except:
            pass
        if (method == "HEAD"):
            res = generateResponse(length, 200, resource, lastModified, par[0],
                                   "HEAD")
            print(res)
        else:
            res = generateResponse(length, 200, resource, lastModified, par[0])
        logger.generate(headers[0], res)
        return res
    except FileNotFoundError:
        res = generateResponse(length, 404)
        logger.generate(headers[0], res)
        return res


def parse_POST_Request(headers):
    # TODO
    # Annotation of existing resources
    # Posting message to an existing bulleting, news board etc
    # Providing a block of data, such as the result of submitting a form, to a data-handling process
    # Extending a database through an append operation.

    # For the purpose of the project, POST methods will write the incoming data into a logs file
    global resource
    global f

    params = {}
    body = []
    for i in headers[1:]:

        try:
            headerField = i[:i.index(':')]
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            if i != '\r' and i != '\n':
                body.append(i)

    path = headers[0].split(' ')[1]

    if (path == "/"):
        path = 'index.html'
    else:
        path = documentRoot + path

    # Check if file at path is write-able else respond with FORBIDDEN response
    if os.path.exists(path):
        if os.access(path, os.W_OK):
            f = open(path, 'rb')
            response_code = 200
        else:
            response_code = 403
    else:
        f = open(path, 'rb')
        response_code = 201

    if (response_code == 403):
        res = generateResponse(0, 403)
        return res

    resource = f.read()

    f2 = open('./logs/post_log.txt', 'w+')
    # Handle application/x-www-form-urlencoded type of data
    content_type = params['Content-Type']
    if "application/x-www-form-urlencoded" in content_type:
        # example string name1=value1&name2=value2
        form_data = {}
        print(body)
        for line in body:
            line = line.split('&')
            for param in line:
                param = param.split('=')
                form_data[param[0]] = param[1]

        f2.write(str(form_data))

    res = generateResponse(len(resource), response_code, resource, None)
    return res


def parse_PUT_Request(headers):
    pass


def parse_HEAD_Request(headers):
    # Returns the response of GET without the message body
    # TODO
    # Add more headers to the repsonse in the reponse.py file
    # Handle Caching with GET
    return parse_GET_Request(headers, "HEAD")


def parse_DELETE_Request(headers):
    global resource
    global f
    global logger
    # TODO
    # The DELETE method requests that the origin server delete the resource identified by the Request-URI.
    # The client cannot be guaranteed that the operation has been carried out,
    # even if the status code returned from the origin server indicates
    # that the action has been completed successfully.
    # However, the server SHOULD NOT indicate success unless, at the
    # time the response is given, it intends to delete the resource or move it to an inaccessible location.
    params = {}
    body = []
    for i in headers[1:]:

        try:
            headerField = i[:i.index(':')]
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            if i != '\r' and i != '\n':
                body.append(i)

    path = headers[0].split(' ')[1]
    path = documentRoot + path

    if os.path.exists(path):
        if os.access(path, os.W_OK):
            os.remove(path)
            # No content response and the request was successful
            res = generateResponse(0, 204)
            logger.generate(headers[0], res)
            return res
        else:
            # Forbidden because delete permission not granted
            res = generateResponse(0, 403)
            logger.generate(headers[0], res)
            return res

    else:
        # File not found error
        res = generateResponse(0, 404)
        logger.generate(headers[0], res)
        return res


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
        print(error)
        return generateResponse(0, 400)


def accept_client(s):

    global resource
    # print("Started a new thread")
    while True:
        client_socket, client_addr = s.accept()

        try:
            while True:
                data = client_socket.recv(5000).decode('utf-8')
                res = process(data)
                if ('\r\n\r\n' in data):
                    break

            client_socket.send(res.encode('utf-8'))
            if (method == "GET"):
                client_socket.send(resource)

        except:
            error = sys.exc_info()[0]
            print(error)
        finally:
            client_socket.close()

    return


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', int(sys.argv[1])))
    s.listen(90)

    print("Listening on port {}".format(sys.argv[1]))
    # TODO
    # Implement with multithreading
    logger = Logger()
    # while 1:
    #     clientsocket, clientaddr = s.accept()
    #     # threading.Thread()
    #     try:
    #         while 1:
    #             data = clientsocket.recv(5000).decode('utf-8')
    #             res = process(data)
    #             if ('\r\n\r\n' in data):
    #                 break

    #         clientsocket.send(res.encode('utf-8'))
    #         if (method == "GET"):
    #             clientsocket.send(resource)
    #     except:
    #         error = sys.exc_info()[0]
    #         print(error)
    #     finally:
    #         clientsocket.close()
    #         # f.close()

    try:
        server_thread = threading.Thread(target=accept_client, args=(s, ))
        server_thread.start()
    except:
        print("Unable to start thread")
