import os
import sys
import json
sys.path.append(os.path.abspath(os.path.join('..')))
from response import *
from logger import Logger
import pathlib
from utils.parser import *
from utils import mediaTypes
from config.config import DOCUMENT_ROOT

documentRoot = DOCUMENT_ROOT
logger = Logger()


def parse_PUT_Request(headers, cli, raw=None):
    # TODO
    # The PUT method requests that the enclosed entity be stored
    # under the supplied Request-URI. If the Request-
    # URI refers to an already existing resource, the enclosed
    # entity SHOULD be considered as a modified version of the
    # one residing on the origin server.

    resource = ''
    f = ''
    logger.client_addr = cli

    params, body = Parser.parse_headers(headers, 'PUT')
    path = headers[0].split(' ')[1]

    if path == '/':
        pass
    else:
        path = documentRoot + path

    # check if the file exists already
    if os.path.exists(path):
        if os.access(path, os.W_OK):
            f1 = open(path, 'wb')
            response_code = 204
        else:
            response_code = 403
            res = generateResponse(0, response_code, body[0])
            print(res)
            logger.generateError(headers[0], res)
            return (res, "")
    else:
        f1 = open(path, 'wb')
        response_code = 201

    content_type = params['Content-Type']
    header_length = len("\n".join(headers[:params['index']]))

    # print(header_length)
    f1.write(raw[header_length + 1:])

    # form_data = Parser.parse_body(content_type, body, "PUT", headers)

    # if ('isFile' in form_data.keys() and form_data['isFile']):

    #     header_length = form_data['header_length']
    #     filedata = raw[:-46][header_length + 1:]
    #     f1.write(filedata)

    # else:
    #     f1.write(json.dumps(form_data, indent=4).encode())

    res = generateResponse(0, response_code, headers[0])
    logger.generate(headers[0], res)
    print(res)
    return (res, "")