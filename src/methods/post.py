import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from response import *
from logger import Logger
import pathlib
from parsers import *

documentRoot = str(pathlib.Path().absolute()) + "/assets/"
logger = Logger()


def parse_POST_Request(headers, cli):
    # TODO
    # Annotation of existing resources
    # Posting message to an existing bulleting, news board etc
    # Providing a block of data, such as the result of submitting a form, to a data-handling process
    # Extending a database through an append operation.

    # For the purpose of the project, POST methods will write the incoming data into a logs file
    resource = ''
    f = ''
    logger.client_addr = cli

    body = []
    params, body = parse_headers(headers)
    path = headers[0].split(' ')[1]
    # print(params)
    if (path == "/"):
        path = documentRoot + 'index.html'
    else:
        path = documentRoot + path

    # Check if file at path is write-able else respond with FORBIDDEN response
    if os.path.exists(path):
        if os.access(path, os.W_OK):
            f = open(path, 'w')
            response_code = 200
        else:
            response_code = 403
    else:
        f = open(path, 'w')
        response_code = 201

    if (response_code == 403):
        res = generateResponse(0, 403)
        logger.generateError(headers[0], res)
        return res

    # Handle application/x-www-form-urlencoded type of data
    content_type = params['Content-Type']
    # print(content_type)

    form_data = parse_body(content_type, body, 'POST')
    logger.generatePOST(str(form_data) + '\n')

    if (form_data['isFile']):
        f.write(form_data['filedata'])

    res = generateResponse(len(body[0]), response_code, body[0], None)
    print(res)
    return (res, "")
