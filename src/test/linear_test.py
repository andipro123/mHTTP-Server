import os
import threading
import sys
import time
import encodings.idna
import http.client
import platform
import ssl
from rich.console import Console

port = sys.argv[1]
n = sys.argv[2]
order = 'parallel'
try:
    order = sys.argv[3]
except:
    pass



console = None

class Thread (threading.Thread):
    def __init__(self, options, n, version):
        threading.Thread.__init__(self)
        self.user_agent = "PyStressTest/{}({} {} {})".format(version, platform.system(), os.name, platform.release())
        self.host = options.host
        self.port = options.port
        self.path = options.path
        self.timeout = options.timeout
        self.n = n
        self.allow_ssl = options.allow_ssl
        self.self_signed = options.self_signed
        self.headers = options.headers
        self.success = False
        self.time = 0

    def run(self):
        try:
            console.print("Request {}: GET on {}".format(self.n, self.path))
            now = time.time()
            if self.allow_ssl:
                if self.self_signed:
                    c = http.client.HTTPSConnection(self.host, self.port, timeout=self.timeout, key_file=None, cert_file=None, context=ssl._create_unverified_context())
                else:
                    c = http.client.HTTPSConnection(self.host, self.port, timeout=self.timeout, key_file=None, cert_file=None)
            else:
                c = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
            self.headers["User-Agent"] = self.user_agent
            c.request(method="GET", url=self.path, headers=self.headers)
            res = c.getresponse()
            processed = round((time.time() - now) * 1000)
            self.print_result(res.status, res.reason, processed)
            self.time = processed
            if res.status < 400:
                self.success = True
        except Exception as e:
            console.print("Request {}: [bold red]{}[/]".format(self.n, e))
            console.print()
    
    def is_succeeded(self):
        return self.success

    def get_time(self):
        return self.time

    def print_result(self, code, reason, processed):
        if code >= 100 and code < 200:
            console.print("Request {}: [cyan]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        elif code >= 200 and code < 300:
            console.print("Request {}: [green]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        elif code >= 300 and code < 400:
            console.print("Request {}: [cyan]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        elif code >= 400 and code < 500:
            console.print("Request {}: [orange]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))
        else:
            console.print("Request {}: [red]{} {}[/] (in [blue]{} ms[/])".format(self.n, code, reason, processed))


def startSerial(thread):
    for t in thread:
        t.run()

def startParallel(thread):
    active = []
    for t in thread:
        t.start()
        active.append(t)
    for s in active:
        if s.is_alive():
            s.join()



def startTest():
    t = []
    for i in range(n):
        t.append(Thread(port,n,order,i))
    if(order == 'serial'):
        startSerial(t)
    else:
        startParallel(t)

