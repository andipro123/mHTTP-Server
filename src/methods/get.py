import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from utils import entityHeaders
from response import *
from logger import Logger
import pathlib
from utils.mediaTypes import mediaTypes
import random
import gzip

documentRoot = str(pathlib.Path().absolute()) + "/assets/"
logger = Logger()
qValue = []

def getExtension(mediaTypes):
    f = {}
    for k in mediaTypes.keys():
        f[mediaTypes[k]] = k
    return f

def generateEtag(time,length):
    return str(int(time)) + str(length)

def matchAccept():
    par = []
    for i in qValue:
        par.append(list(i)[0])
    return par
def parseContentType(content):
    global qValue
    qValue = []
    content = content.split(',')
    for i in content:
        k = i.split(';')
        if(len(k) > 1):
            qValue.append((k[0],float(k[1].split('=')[1])))
    if(qValue == []):
        qValue.append((content[0],1.0))
    qValue.sort(key = lambda x:x[1], reverse = True)
    # print(qValue)
    return qValue

def parse_GET_Request(headers,method=""):
    # TODO
    # Run tests
    params = {}
    for i in headers[1:]:
        try:
            headerField = i[:i.index(':')]
            if(headerField == "Accept"):
                parseContentType(i[i.index(':') + 2: len(i) - 1] )
            params[headerField] = i[i.index(':') + 2:len(i) - 1]
        except :
            pass
    
    # Return 406 on not getting file with desired accept
    par = matchAccept()
    # print(par)
    ctype = ""
    if('*/*' in par or 'text/html' in par):
        ctype = "text/html"
    path = headers[0].split(' ')[1]
    for i in par:
        file = path.split('.')[0] + '.' + i.split('/')[1]
        if os.path.exists(documentRoot + file):
            ctype = i
            break
    length = 0
    if(ctype == ""):
        reqParams = {
            'code' : 406,
            'ctype' : params['Accept'],
            'length' : 0,
            'etag' : ''
        }
        return generateGET(reqParams),""
    # print(ctype)
    try:
        if (path == "/"):
            path = documentRoot + 'index.html'
        else:
            try:
                try:
                    extension ='.' + path.split('.')[1]
                except:
                    extension = '.' + ctype.split('/')[1]
                path = documentRoot + path
            except e:
                print("Exceptions" , e)
                for i in par:
                    if(os.path.exists(documentRoot + i)):
                        ctype = i
                        break
                # ctype = par[0]
        reqParams = {
            'length' : 0,
            'code' : 200,
            'ctype' : ctype,
            'etag' : '',
        }
        
        if('.' not in path.split('\n')[-1]):
            path += '.' + ctype.split('/')[1] 
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
        if('Cookie' in params.keys()):
            reqParams['Cookie'] = params['Cookie']
            
        if (method == "HEAD"):
            # res = generateResponse(length, 200, resource, lastModified, ctype,"HEAD")
            res = generateGET(reqParams)
            print(res)
            return res, ""
        
        #415
        if('Content-Encoding' in params.keys() and params['Content-Encoding'] not in entityHeaders['Content-Encoding']):
            res = generateResponse(0, 415)
            f.close()
            return res, ""
        res = generateGET(reqParams)
        # res = generateResponse(length, 200, resource, lastModified, ctype,Etag)
        
        if('If-None-Match' in params.keys()):
            # e = getEtag(f)
            e = Etag
            if(e == params['If-None-Match']):
                reqParams['code'] = 304
                reqParams['length'] = 0
                return generateGET(reqParams), ""
                # return generateResponse(0, 304, resource, lastModified, ctype),""
                
        
        #Successfull Content Encoding
        if('Content-Encoding' in params.keys()):
            if(params['Content-Encoding'] == 'gzip'):
                res = res[:len(res) - 2] + 'Content-Encoding: gzip' + '\r\n\r\n'
                resource = gzip.compress(resource)
            elif(params['Content-Encoding'] == ''):
                pass
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
        # print(res)
        return res, ""

