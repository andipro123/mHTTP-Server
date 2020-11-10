# Get this from the config file
#  "%h %l %u %t \"%r\" %>s %b"
# Format of the log files:
# [time] req rescode length
from config.config import ACCESS_LOG, ERROR_LOG, POST_LOG
from config.config import LOG_FILE
from config.config import LOG_FORMAT
from config.config import LOG_LEVEL
import threading
import json
import pytz
from datetime import datetime, timedelta
logPath = ACCESS_LOG
postLog = POST_LOG
errorLog = ERROR_LOG


class Logger():
    def __init__(self):
        self.lock = threading.Lock()

    client_addr = ''

    def generate(self, req, res):
        logFile = open(logPath, 'a')
        res = res.split('\n')
        params = {}
        for i in res[1:]:
            try:
                headerField = i[:i.index(':')]
                params[headerField] = i[i.index(':') + 2:len(i) - 1]
            except:
                pass
        code = res[0].split(' ')[1]
        date = params['Date'].split(' ')
        datestr = date[1] + '/' + date[2] + '/' + date[3] + ':' + date[
            4] + " " + date[5]

        log = ''
        for i in LOG_FORMAT.split(' '):
            if (i == " "):
                break
            if (i == 'CLIENT_IP'):
                log += self.client_addr[0] + ' '
            elif (i == '[DATETIME]'):
                log += f'[{datestr}] '
            elif (i == 'REQUEST'):
                log += f' \"{req[:len(req) - 1]}\" '
            elif (i == 'RESPONSE'):
                log += "{} ".format(code)
            elif (i == 'LENGTH'):
                log += "{} ".format(params['Content-Length'])
        # print(log)
        if (log == ''):
            log = "{} [{}] \"{}\" {} {}\n".format(self.client_addr[0], datestr,
                                                  req[:len(req) - 1], code,
                                                  params['Content-Length'])
        self.lock.acquire()
        logFile.write(log + '\n')
        logFile.close()
        self.lock.release()

    def generatePOST(self, data, req, params, code):
        postFile = open(postLog, "a")
        # log = req + res[0] + params['Date'] + '\n'
        date = params.get('Date', None)
        if date:
            datestr = date[1] + '/' + date[2] + '/' + date[3] + ':' + date[
                4] + " " + date[5]
        else:
            today = datetime.today()
            datestr = today.strftime("%a, %d %b %Y %X IST")

        log = ''
        for i in LOG_FORMAT.split(' '):
            if (i == " "):
                break
            if (i == 'CLIENT_IP'):
                log += self.client_addr[0] + ' '
            elif (i == '[DATETIME]'):
                log += f'[{datestr}] '
            elif (i == 'REQUEST'):
                log += f' \"{req[:len(req) - 1]}\" '
            elif (i == 'RESPONSE'):
                log += "{} ".format(code)
            elif (i == 'LENGTH'):
                log += "{} ".format(params['Content-Length'])
        if (log == ''):
            log = "{} [{}] \"{}\" {} {}\n".format(self.client_addr[0], datestr,
                                                  req[:len(req) - 1], code,
                                                  params['Content-Length'])

        form_data = json.dumps(data, indent=4)
        self.lock.acquire()
        postFile.write(log)
        postFile.write(form_data + '\n')
        postFile.close()
        self.lock.release()

    def generateError(self, req, res):
        if (LOG_LEVEL == "-c"):
            return
        file = open('./logs/error_log.txt', "a")
        res = res.split('\n')
        params = {}
        for i in res[1:]:
            try:
                headerField = i[:i.index(':')]
                params[headerField] = i[i.index(':') + 2:len(i) - 1]
            except:
                pass
        code = res[0].split(' ')[1]
        date = params['Date'].split(' ')
        datestr = date[1] + '/' + date[2] + '/' + date[3] + ':' + date[
            4] + " " + date[5]

        log = ''
        for i in LOG_FORMAT.split(' '):
            if (i == " "):
                break
            if (i == 'CLIENT_IP'):
                log += self.client_addr[0] + ' '
            elif (i == '[DATETIME]'):
                log += f'[{datestr}] '
            elif (i == 'REQUEST'):
                log += f' \"{req[:len(req) - 1]}\" '
            elif (i == 'RESPONSE'):
                log += "{} ".format(code)
            elif (i == 'LENGTH'):
                log += "{} ".format(params['Content-Length'])
        if (log == ''):
            log = "{} [{}] \"{}\" {} {}\n".format(self.client_addr[0], datestr,
                                                  req[:len(req) - 1], code,
                                                  params['Content-Length'])

        self.lock.acquire()
        file.write(log + '\n')
        file.close()
        self.lock.release()

    def ServerError(self, e):
        if (LOG_LEVEL == '-r'):
            return
        offset = 0
        date = datetime.now(tz=pytz.utc) + timedelta(seconds=offset)
        time = " {}:{}:{} GMT".format(date.strftime("%H"), date.strftime("%M"),
                                      date.strftime("%S"))
        date = date.strftime("%a") + ', ' + str(
            date.strftime("%d")) + " " + date.strftime("%b") + " " + str(
                date.year) + time

        file = open(errorLog, "a")
        file.write(f"[{date}] {e}\n")
        file.close