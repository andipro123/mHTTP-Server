import os
import threading
import sys
import time
import encodings.idna
import http.client
import platform
from rich.console import Console

port = sys.argv[1]
n = int(sys.argv[2])
order = 'parallel'
try:
    order = sys.argv[3]
except:
    pass



console = Console(highlight=False)

def get_available_threads():
    if sys.platform == 'win32':
        return (int)(os.environ['NUMBER_OF_PROCESSORS'])
    else:
        return (int)(os.popen('grep -c cores /proc/cpuinfo').read())

class Thread (threading.Thread):
    def __init__(self, port, n):
        threading.Thread.__init__(self)
        self.user_agent = "StressTester({} {} {})".format(platform.system(), os.name, platform.release())
        self.host = "localhost"
        self.port = port
        self.n = n
        self.success = False
        self.time = 0
        self.path = "/"
        self.headers = {}

    def run(self):
        try:
            console.print("Request {}: GET on {}".format(self.n, self.path))
            now = time.time()
            self.headers["User-Agent"] = self.user_agent
            c = http.client.HTTPConnection(self.host, self.port,timeout = 1)
            c.request(method="GET", url=self.path,headers=self.headers)
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
        k = get_available_threads()
        if(len(active) >= k):
            for s in active:
                if s.is_alive():
                    s.join()
                active.clear()
    for s in active:
        if s.is_alive():
            s.join()



def startTest():
    t = []
    success = 0
    for i in range(n):
        t.append(Thread(port,i))
    if(order == 'serial'):
        startSerial(t)
    else:
        startParallel(t)
    for i in t:
        if i.is_succeeded():
            success += 1
    console.print("Success: {}\nFailures: {}\n".format(success, n - success))
    # startSerial(t)
    # startParallel(t)

if __name__ == "__main__":
    startTest()
