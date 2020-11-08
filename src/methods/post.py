import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('config')))
from response import *
from logger import Logger
import pathlib
from utils.parser import *
from config.config import DOCUMENT_ROOT

documentRoot = DOCUMENT_ROOT
logger = Logger()


def parse_POST_Request(headers, cli, raw=None):
    # TODO
    # Annotation of existing resources
    # Posting message to an existing bulleting, news board etc
    # Providing a block of data, such as the result of submitting a form, to a data-handling process
    # Extending a database through an append operation.

    # For the purpose of the project, POST methods will write the incoming data into a logs file
    logger.client_addr = cli
    resource_len = len(raw)

    params, body = Parser.parse_headers(headers, 'POST')
    path = headers[0].split(' ')[1]
    if (path == "/"):
        path = documentRoot
    else:
        path = documentRoot + path

    # Check if file at path is write-able else respond with FORBIDDEN response
    if os.path.exists(path):
        # f = open(path, 'wb')
        response_code = 204
    else:
        # f = open(path, 'wb')
        response_code = 201

    # if (response_code == 403):
    #     res = generateResponse(0, 403)
    #     logger.generateError(headers[0], res)
    #     return res

    # Handle application/x-www-form-urlencoded type of data
    content_type = params['Content-Type']

    form_data = Parser.parse_body(content_type, body, 'POST', headers)

    if ('isFile' in form_data.keys() and form_data['isFile']):

        header_length = form_data['header_length']
        form_data['filedata'] = str(raw[:-46][header_length + 1:])

    res = generateResponse(len(body[0]), response_code, body[0], None)
    logger.generate(headers[0], res)
    logger.generatePOST(form_data, headers[0], params, response_code)
    print(res)
    return (res, "")
