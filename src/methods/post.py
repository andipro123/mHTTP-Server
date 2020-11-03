import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from response import *
from logger import Logger
import pathlib
from parsers import *

documentRoot = str(pathlib.Path().absolute()) + "/assets/"
logger = Logger()


def parse_POST_Request(headers, cli, raw=None):
    # TODO
    # Annotation of existing resources
    # Posting message to an existing bulleting, news board etc
    # Providing a block of data, such as the result of submitting a form, to a data-handling process
    # Extending a database through an append operation.

    # For the purpose of the project, POST methods will write the incoming data into a logs file
    resource = ''
    f = ''
    logger.client_addr = cli
    resource_len = len(raw)

    body = []
    params, body = parse_headers(headers)
    # print('BODYYYYY: ', body[12:]))
    path = headers[0].split(' ')[1]
    # print(params)
    if (path == "/"):
        path = documentRoot
    else:
        path = documentRoot + path

    # Check if file at path is write-able else respond with FORBIDDEN response
    if os.path.exists(path):
        if os.access(path, os.W_OK):
            # f = open(path, 'wb')
            response_code = 200
        else:
            response_code = 403
    else:
        # f = open(path, 'wb')
        response_code = 201

    if (response_code == 403):
        res = generateResponse(0, 403)
        logger.generateError(headers[0], res)
        return res

    # Handle application/x-www-form-urlencoded type of data
    content_type = params['Content-Type']
    # print(content_type)

    form_data = parse_body(content_type, body, 'POST', headers)
    logger.generatePOST(str(form_data) + '\n')

    print('FORMDATA:', form_data)
    # print(form_data['filename'])
    if ('isFile' in form_data.keys() and form_data['isFile']):
        try:
            f = open(path + form_data['filename'], 'wb')
            # print(raw[:-46][-form_data['filesize']:])
            header_length = form_data['header_length']
            f.write(raw[:-46][header_length + 1:])
        except:
            pass

    res = generateResponse(len(body[0]), response_code, body[0], None)
    print(res)
    return (res, "")
