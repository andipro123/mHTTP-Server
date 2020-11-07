# Get this from the config file
#  "%h %l %u %t \"%r\" %>s %b"
# Format of the log files:
# [time] req rescode length
from config.config import LOG_FILE
import threading
import pytz
from datetime import datetime, timedelta
logPath = LOG_FILE



#TODO
# Add the host ip to the request
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
        # log = req + res[0] + params['Date'] + '\n'
        code = res[0].split(' ')[1]
        date = params['Date'].split(' ')
        datestr = date[1] + '/' + date[2] + '/' + date[3] + ':' + date[
            4] + " " + date[5]

        log = "{} [{}] \"{}\" {} {}\n".format(self.client_addr[0],datestr, req[:len(req) - 1], code,
                                           params['Content-Length'])
        self.lock.acquire()
        logFile.write(log)
        logFile.close()
        self.lock.release()

    def generatePOST(self, data):
        file = open('./logs/post_log.txt', "a")
        file.write(str(data))
        file.close()

    def generateError(self, req, res):
        file = open('./logs/error_log.txt', "a")
        res = res.split('\n')
        params = {}
        for i in res[1:]:
            try:
                headerField = i[:i.index(':')]
                params[headerField] = i[i.index(':') + 2:len(i) - 1]
            except:
                pass
        # log = req + res[0] + params['Date'] + '\n'
        code = res[0].split(' ')[1]
        date = params['Date'].split(' ')
        datestr = date[1] + '/' + date[2] + '/' + date[3] + ':' + date[
            4] + " " + date[5]

        log = "{} [{}] \"{}\" {} {}\n".format(self.client_addr[0], datestr,
                                              req[:len(req) - 1], code,
                                              params['Content-Length'])

        file.write(log)
        file.close()

    def ServerError(self,e):
        offset = 0
        date = datetime.now(tz=pytz.utc) + timedelta(seconds = offset)
        time = " {}:{}:{} GMT".format(date.strftime("%H"), date.strftime("%M"),date.strftime("%S"))
        date = date.strftime("%a") + ', ' + str(date.strftime("%d")) + " " + date.strftime("%b") + " " + str(date.year) + time

        file = open('./logs/error_log.txt', "a")
        file.write(f"[{date}] {e}\n")
        file.close