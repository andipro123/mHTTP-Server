import pathlib

#Global Configuration
DOCUMENT_ROOT = str(pathlib.Path().absolute()) + '/assets/'

#Default timeout
TIMEOUT = 500

#Default port number
PORT = 5002

#Maximum number of conncetions supported simulataneously
MAX_CONNECTIONS = 3000

#Access Log File directory
LOG_FILE = str(pathlib.Path().absolute()) + '/logs/access_log.txt'

#Define the format as follows:
#CLIENT_IP => Show to IP address of the client that has made the request
#DATETIME => Show the Date and Time Stamp of the request
#REQUEST => Show the requested asset and method
#RESPONE => Show the response code and message
#LENGTH => Show the length of the content served
LOG_FORMAT = "CLIENT_IP [DATETIME] REQUEST RESPONSE"

#Log levels 
#-c Critical System crashes
#-r Request Errors
#-all All errors
LOG_LEVEL = "-all"
