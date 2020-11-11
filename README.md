<p align="center">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">mHTTP Server</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> mHTTP Server is an HTTP/1.1 compliant web server and is aimed at implementing some common methods for exchanging information.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Usage](#usage)
- [Running Tests](#tests)
- [Logging](#log)
- [Deployment](#deployment)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This project is aimed at the implementation of the HTTP/1.1 Protocol based on RFC 2616 and incorporates the basic HTTP methods of GET, POST, PUT, DELETE and HEAD.

### Prerequisites

1. Python 3.x

For installing necessary dependencies before running the project run the following command:

```
pip3 install -r requirements.txt
```

### 🏁 Usage <a name = "usage"></a>

Follow the below steps to start the server

```
cd src
./start.sh
```

This will start the server on a default port of as mentioned in the configuration file. To specify custom configuration edit the config file in the config/ directory. The following options are available in the config file

```
1. PORT = Specify the port on which the server will keep listenting
2. DOCUMENT_ROOT = Specify the document root directory that will serve the requests
3. MAX_CONNECTIONS = Specify the maximum number of simultaneous connections that the server will accept
4. DEFAULT_TIMEOUT = Specify the Timeout value for the response
5. ACCESS_LOG = Specify the file to save access logs
6. ERROR_LOG = Specify the file to save error logs
7. POST_LOG = Specify the file to save post logs
8. LOG_FORMAT = Specify the format to write access logs from the server
9. LOG_LEVEL = Specify the levels for error logs from the server
10. WATCHED_FILES = Specify files to watch for hot reload
```

Once the server starts, it will start a background process that serves connections from clients.
To stop the server do the following:

```
[cd src]
./stop.sh
```

To restart the server do the following:

```
[cd src]
./restart.sh
```

## 🔧 Running the tests <a name = "tests"></a>

Automated test scripts to test the specified functionalities can be found in the `/src/test/` directory

### Automated Unit Tests

These tests ensure the conformance of the basic functionalities and the correctness of the responses. All the supported methods are tested and variable paramters can be tuned to test specific scenarios.

#### To run unit test module do the following:

```
[cd src/test/]
python3 unitTest.py PORT-NO [options]
```

```
The options specifications for the test module:
1. -g Test the GET method alongwith some edge cases for handling headers
2. -p Test the POST method with a dummy form data
3. -pt Test the PUT method with dummy form data/byte data
4. -h Test the HEAD method
5. -d Test the DELETE method
6. -cg Test the Conditional GET method
7. -m Test a combination of the 5 methods
8. -e Test with a malformed request
8. -go-crazy Simulate a parallel combination of multiple methods
```

#### To run tests for cookies:

1. Run an instance of the server
2. Go to a browser and type the url <a>http://localhost:[PORT]/login.html</a>
3. The page will simulate a login state management using cookies that expires every 15 seconds.
   <b>Expected behaviour: </b> Shows the <i>logged out refresh again </i>screen by default. Upon refreshing a new cookie is obtained from the server and is cached locally. For every subsequent request the cookies are sent from the client. Upon expiration the <i>logged out refresh again</i> page will reappear.

Alternately you can also run a python script in the `src/test/` directory to send a request and observe the recieved cookie

### Automated Stress Tests

These tests check if the server can handle a large scale pool of network requests in parallel and serve the reponses.

#### To run stress test module do the following:

```
[cd src/test/]
python3 stressTest.py PORT-NO CONNECTIONS
```

Example:

```
python3 stressTest.py 5000 100

Tries to send 100 parallel requests to the server listening on port 5000
```

## ✍️ Logs <a name="log"></a>

The logs to the server requests as well as internal server state can be viewed in the `src/logs` directory. There are three types of logs maintained by the server:

1. Access Logs
2. Error Logs
3. POST Request Logs

<b>Access Logs</b>
Keeps track of all the requests served successfully by the server alongwith the response code. The default format of the access logs:

```
CLIENT_IP [DATETIME] REQUEST RESPONSE  LENGTH
```

The log format can be changed from the config file to match a desired format.

<b>Error Logs</b>
Keeps track of internal server errors and the requests that caused the error.The format of error logs:

```
CLIENT_IP [DATETIME] REQUEST RESPONSE LENGTH | CLIENT_IP ERROR_NO ERROR_MSG
```

Error logs also include levels of logging.
The following parameters can be used in the config file to record the desired error logs from the server.

```
1. -c = Records all critical server crashes and errors within the server.
2. -r = Records all error requests that were recieved to the server. Includes the 4xx and 5xx series responses
3. -all = Records all the erros inclusive of server state and error requests.
```

<b>Access Logs</b>
Keeps track of all the POST requests served successfully by the server alongwith the response code. The default format of the access logs:

```
CLIENT_IP [DATETIME] REQUEST RESPONSE LENGTH {FORM_DATA in json format}
```

The log format can be changed from the config file to match a desired format.

A log compressor script is also included with the log files that can be run to compress and store the log files into a different directory. The script can be cron scheduled to save disk space once the log file size exceeds a certain limit.

## 🚀 Deployment <a name = "deployment"></a>

The server is running live on AWS. The link to the server is <a>to be added</a>

## ⛏️ Built Using <a name = "built_using"></a>

- Python - Server Environment

## ✍️ Authors <a name = "authors"></a>

- [@AnupNair08](https://github.com/AnupNair08)
- [@andipro123](https://github.com/andipro123)

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [RFC2616](https://tools.ietf.org/html/rfc2616)
- [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP)
