import pathlib

#Global Configuration
DOCUMENT_ROOT = str(pathlib.Path().absolute()) + '/assets/'

#Default timeout
TIMEOUT = 500

#Default port number
PORT = 5000

#Maximum number of conncetions supported simulataneously
MAX_CONNECTIONS = 300

#Access Log File directory
LOG_FILE = str(pathlib.Path().absolute()) + '/logs/access_log.txt'