# Get this from the config file
logPath = './logs/access_log.txt'


#  "%h %l %u %t \"%r\" %>s %b"
# Format of the log files:
# [time] req rescode length

#TODO
# Add the host ip to the request
class Logger():
    def __init__(self):
        pass

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
        datestr = date[1] + '/' + date[2] + '/' + date[3] + ':' + date[4] + " " + date[5]

        log = "[{}] \"{}\" {} {}\n".format(datestr,req[:len(req) - 1],code,params['Content-Length'])
        logFile.write(log)  
        logFile.close()
    
    def generatePOST(self,data):
        file = open('./logs/post_log.txt',"a")
        file.write(str(data))
        file.close()
    
    def generateError(self,data):
        file = open('./logs/error_log.txt',"a")
        res = "Error generated with code {}".format(data)
        file.write(res)
        file.close()
