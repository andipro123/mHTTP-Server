documentRoot = ''
import os
from response import *


def parse_GET_Request(headers):
    # TODO
    # Implement Conditional Get
    # Implement Range Header
    # MIME Encoding response
    params = {}
    for i in headers[1:]:
        headerField = i[:i.index(':')]
        params[headerField] = i[i.index(':') + 2:len(i) - 1]

    print(params)
    path = headers[0].split(' ')[1]
    path = documentRoot + path
    # print(path)
    try:
        if (path == "/"):
            path = 'index.html'
        f = open(path, "r")
        print("OK")
        return "200"  #Proper data encoding and sending as a HTTP response
    except FileNotFoundError:
        print("NOT OK")
        return "404"  #Change to proper HTTP response


def parse_POST_Request(headers):
    # TODO
    # Annotation of existing resources
    # Posting message to an existing bulleting, news board etc
    # Providing a block of data, such as the result of submitting a form, to a data-handling process
    # Extending a database through an append operation.

    # For the purpose of the project, POST methods will write the incoming data into a logs file

    params = {}
    body = []
    for i in headers[1:]:

        try:
            headerField = i[:i.index(':')]
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except:
            body.append(i)

    # print(params)
    # print(body)
    path = headers[0].split(' ')[1]
    path = documentRoot + path

    if (path == "/"):
        path = 'index.html'

    # Check if file at path is write-able else respond with FORBIDDEN response
    if os.path.exists(path):
        if os.access(path, os.W_OK):
            f1 = open(path, 'w')
            response_code = 200
        else:
            response_code = 403
    else:
        f1 = open(path, 'w')
        response_code = 201

    if response_code == 403:
        res = generateResponse(403)
        return res

    f2 = open('./logs/post_log.txt', 'w')

    # Handle application/x-www-form-urlencoded type of data
    content_type = params['Content-Type']
    print(content_type)
    form_data = {}
    if "application/x-www-form-urlencoded" in content_type:
        print('Hi')
        # example string name1=value1&name2=value2

        for line in body:
            line = line.split('&')
            for param in line:
                param = param.split('=')
                form_data[param[0]] = param[1]
        print(str(form_data))
        f2.write(str(form_data))

    res = generateResponse(form_data, response_code)
    return res


f = open("req2.txt", "r")
headers = f.readlines()
parse_POST_Request(headers)