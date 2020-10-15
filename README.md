# mHTTP Server

## An implementation of the HTTP protocol based on RFC 2616

## Overview

mHTTP server aims to implement the HTTP 1.1 protocol and some common methods for exchanging information.

Current progress:

1. Multithreaded server for accepting multiple connections via sockets.
2. Handle the HTTP request by parsing and generating required responses according to the methods.
3. Skeletal implementation of GET is worked on. POST, DELETE and HEAD are working as expected with few improvements to be done.
4. Added a basic logger for generating server logs. (Access logs handled)

WIP:

1. Cache and additional get methods

GET, POST, PUT, HEAD, DELETE,
Cookies,
Headers,
non-persistent connections,
Multiple clients at the same time (with a sepearate program to test this),
logging with levels of logging,
handling file permissions;
Server configuration - config file with DocumentRoot, log file name, max simulateneous connections ;
way to stop and restart the server;
