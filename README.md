<p align="center">
  <a href="" rel="noopener">
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
- [Getting Started](#getting_started)
- [Running Tests](#tests)
- [Logging](#log)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

This project is aimed at the implementation of the HTTP/1.1 Protocol based on RFC 2616 and incorporates the basic HTTP methods of GET, POST, PUT, DELETE and HEAD.

### Prerequisites

1. Python 3.x

### 🏁 Starting the Server <a name = "getting_started"></a>

Follow the below steps to start the server

```
cd src
./start.sh
```

This will start the server on a default port of as mentioned in the configuration file. To specify custom configuration edit the config file in the config/ directory. The following options are available in the config file

```
PORT = Specify the port on which the server will keep listenting
DOCUMENT_ROOT = Specify the document root directory that will serve the requests
MAX_CONNECTIONS = Specify the maximum number of simultaneous connections that the server will accept
DEFAULT_TIMEOUT = Specify the Timeout value for the response
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
python3 unittest.py PORT-NO [options]
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
8. -go-crazy Simulate a parallel combination of multiple methods
```

#### To run tests for cookies:

1. Run an instance of the server
2. Go to a browser and type the url <a>http://localhost:[PORT]/login.html</a>
3. The page will simulate a login state management using cookies that expires every 15 seconds.
   <b>Expected behaviour: </b> Shows the <i>logged out refresh again </i>screen by default. Upon refreshing a new cookie is obtained from the server and is cached locally. For every subsequent request the cookies are sent from the client. Upon expiration the <i>logged out refresh again</i> page will reappear.

### Automated Stress Tests

These tests check if the server can handle a large scale pool of network requests in parallel and serve the reponses.

#### To run stress test module do the following:

```
[cd src/test/]
python3 thread_test.py PORT-NO CONNECTIONS
```

Example:

```
python3 thread_test.py 5000 100

Tries to send 100 parallel requests to the server listening on port 5000
```

## ✍️ Logs <a name="log"></a>

The logs to the server requests as well as internal server state can be viewed in the `src/logs` directory. There are two types of logs maintained by the server:

1. Access Logs
2. Error Logs

<b>Access Logs</b>
Keeps track of all the requests served successfully by the server alongwith the response code. The format of the access logs:

```
client_ip [DATE_STAMP] HTTP_METHOD RESPONSE_CODE CONTENT_LENGTH
```

<b>Error Logs</b>
Keeps track of internal server errors and the requests that caused the error.The format of error logs:

```
client_ip [DATE_STAMP] HTTP_METHOD RESPONSE_CODE CONTENT_LENGTH
```

Error logs also include levels of logging

A log compressor script is also included with the log files that can be run to compress and store the log files into a different directory. The script can be cron scheduled to save disk space.

## 🎈 Usage <a name="usage"></a>

Upon startup the server will start listening for connections on the PORT. The five methods can be used to send HTTP requests to the server.

## 🚀 Deployment <a name = "deployment"></a>

The server is running live on AWS. The link to the server is <a>to be added</a>

## ⛏️ Built Using <a name = "built_using"></a>

- Python - Server Environment

## ✍️ Authors <a name = "authors"></a>

- [@AnupN08](https://github.com/AnupN08)
- [@andipro123](https://github.com/andipro123)

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- [RFC2616](https://tools.ietf.org/html/rfc2616)
- [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP)
