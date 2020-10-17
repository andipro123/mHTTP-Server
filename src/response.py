import pytz
from datetime import datetime, timedelta
from utils.statusCodes import codes
from utils.responseHeaders import responseHeaders
from utils.entityHeaders import entityHeaders
import random

# Response = Status Line + Response Headers + Entity Headers + Entity Body

def getTime(offset = 0):

    date = datetime.now(tz=pytz.utc) + timedelta(seconds = offset)
    time = " {}:{}:{} GMT".format(date.strftime("%H"), date.strftime("%M"),date.strftime("%S"))
    date = date.strftime("%a") + ', ' + str(date.strftime("%d")) + " " + date.strftime("%b") + " " + str(date.year) + time
    return date

def metaData(code):
    date = getTime()
    statusLine = "HTTP/1.1 {} {}\r\n".format(code, codes[code])
    responseheaders = "Server: mHTTP-Alpha1\r\n"
    return date, statusLine + responseheaders

def setCookie():
    #Generate a random integer as a cookie value along with some text and send it
    #Expires: Lifetime of the cookie in the browser
    #Path: sends cookie only if the path is present in the URL
    #Domain: access to the allowed set of domains
    #Secure: Cookie is sent over secure HTTPS requests
    #HttpOnly: Cookie cant be accessed by javascript API
    cookie =  "cook" + str(random.randint(1,5000)) + "ie"
    user = "dev1"
    Expires = getTime(4)
    Path = "/cart"
    Domain = ""  #Serves all hosts
    # f = open('./test/data.txt', "a")
    # f.write(cookie + ":" + user + '\n')
    # f.close()
    cookieHeader =  "Set-Cookie: cID={}; Expires={}; Path={};Domain = {};\r\n".format(cookie, Expires,Path, Domain)
    # print(cookieHeader)
    return cookieHeader


def generateGET(headers):
    code = headers['code']
    if (code not in codes.keys()):
        return
    date, response = metaData(code)
    entityheaders = "Content-Type: {}\r\nDate: {}\r\nContent-Length: {}\r\nConnection: keep-alive\r\nAllow: {}\r\n".format(
    headers['ctype'], date, headers['length'], entityHeaders['Allow'])
    etag = headers['etag']
    if(etag != ''):
        if('Cookie' not in headers.keys()):
            entityheaders += setCookie()
        entityheaders += 'E-Tag: {}\r\n\r\n'.format(headers['etag'])
    else:
        if('Cookie' not in headers.keys()):
            entityheaders += setCookie() + '\r\n'
    # setCookie()
    return response + entityheaders


def generateResponse(length,code,resource=None,lastModified=None,ctype="text/html;charset=UTF-8",method="",encoding="gzip",etag="changelater"):
    if (code not in codes.keys()):
        return
    
    date , response = metaData(code)

    # lastModified = datetime.datetime(int(lastModified))
    # if(ctype != "text/html;charset=UTF-8"):
    #     ctype = ctype
    # print(ctype)

    entityheaders = "Content-Type: {}\r\nDate: {}\r\nContent-Length: {}\r\nConnection: keep-alive\r\nSet-Cookie: anup=nair\r\nAllow: {}\r\nE-Tag: {}\r\n\r\n".format(
        ctype, date, length, entityHeaders['Allow'],etag)
    if(etag == ''):
        #remove the etag header
        pass
    return response + entityheaders
