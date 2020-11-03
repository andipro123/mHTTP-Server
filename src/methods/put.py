import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from response import *
from logger import Logger
import pathlib
from parsers import *
from utils import mediaTypes

documentRoot = str(pathlib.Path().absolute()) + "/assets/"
logger = Logger()


def parse_PUT_Request(headers, cli):
    # TODO
    # The PUT method requests that the enclosed entity be stored
    # under the supplied Request-URI. If the Request-
    # URI refers to an already existing resource, the enclosed
    # entity SHOULD be considered as a modified version of the
    # one residing on the origin server.

    resource = ''
    f = ''
    logger.client_addr = cli

    body = []
    params, body = parse_headers(headers)
    path = headers[0].split(' ')[1]

    if path == '/':
        pass
    else:
        path = documentRoot + path

    # check if the file exists already
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
        res = generateResponse(0, 403)
        logger.generateError(headers[0], res)
        return res

    content_type = params['Content-Type']

    body = parse_body(content_type, body, "PUT")
    #logger
    f1.write(body['filedata'])

    return generateResponse(0, response_code, body[0])