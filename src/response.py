import pytz
import datetime
from utils.statusCodes import codes
from utils.responseHeaders import responseHeaders
from utils.entityHeaders import entityHeaders

#Response = Status Line + Response Headers + Entity Headers + Entity Body


def generateResponse(length,
                     code,
                     resource=None,
                     lastModified=None,
                     ctype="text/html;charset=UTF-8",
                     encoding="gzip"):
    if (code not in codes.keys()):
        return
    date = datetime.datetime.now(tz=pytz.utc)
    time = " {}:{}:{} GMT".format(date.strftime("%H"), date.strftime("%M"),
                                  date.strftime("%S"))
    date = date.strftime("%a") + ', ' + str(
        date.strftime("%d")) + " " + date.strftime("%b") + " " + str(
            date.year) + time

    # lastModified = datetime.datetime(int(lastModified))
    # if(ctype != "text/html;charset=UTF-8"):
    #     ctype = ctype
    print(ctype)
    statusLine = "HTTP/1.1 {} {}\r\n".format(code, codes[code])
    responseHeaders = "Server: mHTTP-Alpha0\r\n"

    entityheaders = "Content-Type: {}\r\nDate: {}\r\nContent-Length: {}\r\n\r\n".format(
        ctype, date, length, encoding)
    body = resource
    return statusLine + responseHeaders + entityheaders
