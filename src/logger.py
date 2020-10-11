# Get this from the config file
logPath = './logs/get_log.txt'

# Log format
# Req <> Status Line <> Timestamp


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
        log = req + res[0] + params['Date'] + '\n'
        logFile.write(log)
        logFile.close()
    
    def generatePOST(self,data):
        file = open('./logs/post_log.txt',"a")
        file.write(str(data))
        file.close()
