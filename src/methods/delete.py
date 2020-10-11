import os
from logger import Logger
from response import generateResponse
import pathlib

documentRoot = str(pathlib.Path().absolute()) + "/assets/"
logger = Logger()

def parse_DELETE_Request(headers):
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
