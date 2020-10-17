import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from utils import entityHeaders
from response import *
from logger import Logger
import pathlib
from utils.mediaTypes import mediaTypes
import random

documentRoot = str(pathlib.Path().absolute()) + "/assets/"
logger = Logger()

def getExtension(mediaTypes):
    f = {}
    for k in mediaTypes.keys():
        f[mediaTypes[k]] = k
    return f

def generateEtag(time,length):
    return str(int(time)) + str(length)
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
    ctype = "text/html"
    try:
        if (path == "/"):
            path = documentRoot + 'index.html'
        else:
            try:
                extension ='.' + path.split('.')[1]
                ctype = getExtension(mediaTypes)[extension]
                path = documentRoot + path
            except:
                ctype = par[0]
        reqParams = {
            'length' : 0,
            'code' : 200,
            'ctype' : ctype,
            'etag' : '',
        }
        if(reqParams['ctype'] == "text/html" and path[len(path) - 4:] != 'html'):
            path = documentRoot + path + '.html'
            # print(path)
        f = open(path, "rb")
        resource = f.read()
        lastModified = os.path.getmtime(path)
        Etag = generateEtag(lastModified,len(resource))
        try:
            length = len(resource)
        except:
            pass
        reqParams['etag'] = Etag
        reqParams['length'] = length
        if (method == "HEAD"):
            # res = generateResponse(length, 200, resource, lastModified, ctype,"HEAD")
            res = generateGET(reqParams)
            print(res)
            return res, ""
        else:
            #415
            if('Content-Encoding' in params.keys() and params['Content-Encoding'] not in entityHeaders['Content-Encoding']):
                res = generateResponse(0, 415)
                f.close()
                return res, ""
            res = generateGET(reqParams)
            # res = generateResponse(length, 200, resource, lastModified, ctype,Etag)
        
        if('cookie' in params.keys()):
            print(params['cookie'])
            print("in")

        if('If-None-Match' in params.keys()):
            # e = getEtag(f)
            e = Etag
            if(e == params['If-None-Match']):
                reqParams['code'] = 304
                reqParams['length'] = 0
                return generateGET(reqParams), ""
                # return generateResponse(0, 304, resource, lastModified, ctype),""
                
        
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
        reqParams['code'] = 404
        reqParams['length'] = 0
        # res = generateResponse(length, 404)
        res = generateGET(reqParams)
        logger.generate(headers[0], res)
        print(res)
        return res, ""

