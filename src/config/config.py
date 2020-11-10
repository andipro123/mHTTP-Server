import pathlib

#Global Configuration
DOCUMENT_ROOT = str(pathlib.Path().absolute()) + '/assets/'

#Default timeout
TIMEOUT = 500

#Default port number
PORT = 5000

#Maximum number of conncetions supported simulataneously
MAX_CONNECTIONS = 3000

#Access Log File directory
ACCESS_LOG = str(pathlib.Path().absolute()) + '/logs/access_log.txt'

#Error Log File Directory
ERROR_LOG = str(pathlib.Path().absolute()) + '/logs/error_log.txt'

#POST Request logs
POST_LOG = str(pathlib.Path().absolute()) + '/logs/post_log.txt'
