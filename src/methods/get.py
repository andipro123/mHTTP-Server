import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from utils import entityHeaders
from response import generateResponse
from logger import Logger
import pathlib

documentRoot = str(pathlib.Path().absolute()) + "/assets/"
logger = Logger()


def matchAccept(headers):
    k = headers.split(',')
    par = []
    for i in k:
        par.append(i)
    return par


def parse_GET_Request(headers,method=""):
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
    if ('Cookie' in params.keys()):
        print(params['Cookie'])
    # Return 406 on not getting file with desired accept
    par = matchAccept(params['Accept'])
    path = headers[0].split(' ')[1]
    length = 0
    try:
        if (path == "/"):
            path = documentRoot + 'index.html'
        else:
            path = documentRoot + path
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
            return res, ""
        else:
            #415
            if('Content-Encoding' in params.keys() and params['Content-Encoding'] not in entityHeaders['Content-Encoding']):
                res = generateResponse(0, 415)
                f.close()
                return res, ""
            res = generateResponse(length, 200, resource, lastModified, par[0])
        
        if('If-None-Match' in params.keys()):
            # e = getEtag(f)
            e = "Anup"
            if(e == params['If-None-Match']):
                return generateResponse(0, 304, resource, lastModified, par[0]),""
                
        
        #Successfull Content Encoding
        if('Content-Encoding' in params.keys() and params['Content-Encoding'] == 'gzip'):
            res = res[:len(res) - 2] + 'Content-Encoding: gzip' + '\r\n\r\n'
        #Check at end
        if('Accept-Ranges' in params.keys()):
            k = int(params['Accept-Ranges'])
            resRange = resource[:k]
            res = res[:len(res) - 2] + 'Accept-Ranges: {}'.format(k) + '\r\n\r\n'
            resource = resRange
        
        logger.generate(headers[0], res)
        print(res)
        f.close()
        return res , resource

    except FileNotFoundError:
        res = generateResponse(length, 404)
        logger.generate(headers[0], res)
        return res, ""

