import requests
import sys
from rich import box
from rich.console import Console
from rich.table import Table
import threading
import pathlib

console = Console(highlight=False)

# -g for GET
# -h for HEAD
# -p for POST
# -pt from PUT
# -d for delete
# -cg for conditional get

options = []
k = len(sys.argv)
try:
    for i in range(2, k):
        options.append(sys.argv[i])
except:
    pass


class UnitTest:
    def __init__(self):
        self.port = sys.argv[1]
        self.url = "http://localhost:{}/".format(self.port)
        # self.url = "http://34.237.242.80:5002/"
        self.lock = threading.Lock()

    def printResult(self, r, expectedCode):
        table = Table(title="Result", box=box.ASCII)
        table.add_column("Method")
        table.add_column("Response", style="green")
        table.add_column("Message", style="blue")
        table.add_column("Test Result")
        code = r.status_code
        if (code in expectedCode):
            result = '[green]Success'
        else:
            result = '[red]Failed'
        table.add_row(r.request.method, str(r.status_code), r.reason, result)
        console.print(table)

    def TestMultipleMethods(self):
        # methods = ['get','head','post','put']
        data = {'name': 'UnitTest1.0', 'tester': 'dev1'}
        console.print('[cyan]Testing GET')
        r = requests.get(self.url)
        self.printResult(r, set([200]))

        console.print('[cyan]Testing POST')
        r = requests.post(self.url, data=data)
        self.printResult(r, set([204, 201, 200]))

        console.print('[cyan]Testing HEAD')
        r = requests.head(self.url)
        self.printResult(r, set([200]))

        console.print('[cyan]Testing PUT')
        r = requests.put(self.url, data=data)
        self.printResult(r, set([204, 201, 200]))

        r = requests.delete(self.url + 'deleteme.txt')
        self.printResult(r, set([204]))

    def TestGET(self):
        url = [
            'test.pdf', 'test.png', 'test.html', 'login.html', 'File', 'test'
        ]
        for i in url:
            r = requests.get(self.url + i)
            if (r.status_code == 404):
                self.printResult(r, set([404]))
            else:
                self.printResult(r, set([200]))
            console.print('Body Length: ', len(r.text))

        self.TestBadCType()
        self.TestQ()
        self.TestBadAccept()
        self.TestRange()

    def TestBadCType(self):
        console.print("[red]Testing Non Existing content type")
        r = requests.get(self.url, headers={'Content-Encoding': 'NotExistent'})
        self.printResult(r, set([415]))
        console.print('Body Length: ', len(r.text))

    def TestQ(self):
        #Q parameter to request for specific data types
        #Based on the values mentioned for each type the highest value will be returned if available
        #If no matching value is requested then send 406
        types = {'application/pdf': 0.3, 'image/png': 0.4, 'ai/ai': 1.0}
        s = ''
        for k in types.keys():
            s += k + ';q={}'.format(types[k]) + ','
        r = requests.get(self.url + 'test', headers={'Accept': s})
        console.print(
            '[red]Testing variable accept type according to priority')
        if (r.status_code == 406):
            self.printResult(r, set([406]))
        else:
            self.printResult(r, set([200]))
        console.print('Body Length:', len(r.text))

    def TestBadAccept(self, Atype="test/html"):
        console.print('[red]Testing a wrong Accept Type')
        r = requests.get(self.url, headers={'Accept': Atype})
        self.printResult(r, set([406]))

    def TestHEAD(self):
        url = [
            'test.pdf', 'test.png', 'test.html', 'login.html', 'File', 'test'
        ]
        for i in url:
            r = requests.head(self.url + i)
            if (r.status_code == 404):
                self.printResult(r, set([404]))
            else:
                self.printResult(r, set([200]))
            console.print('Body Length: ', len(r.text))

    def TestRange(self):
        console.print('[red]Testing Range Headers')
        r1 = requests.head(self.url)
        length = int(r1.headers['Content-Length'])
        console.print('Requesting 10 bytes less')
        r2 = requests.get(self.url,
                          headers={'Accept-Ranges': str(length - 10)})
        console.print(f"Content Length received : {len(r2.text)}")
        self.printResult(r2, set([200]))

    # Expected to fetch the Etag from the server and send this in the next request.
    # Returns 304 if the resource is not modified
    # To check either ways send an optional string as Etag and the resource will be sent with 200
    def TestConditionalGET(self, etag=""):
        url = self.url + "test.pdf"
        console.print("Getting metadata about the resource.")
        r = requests.head(url)
        self.printResult(r, set([200]))
        console.print("Checking if the resource is modified.")
        if (etag == ""):
            try:
                etag = r.headers['E-Tag']
                r = requests.get(url, headers={'If-None-Match': etag})
            except:
                return
        else:
            r = requests.get(url, headers={'If-None-Match': etag})
        self.printResult(r, set([304]))

    def TESTdelete(self):
        r = requests.delete(self.url + 'deleteme.txt')
        self.printResult(r, set([200, 204]))

    def TestPost(self):
        console.print('[red]Testing form data')
        payload = {"name": "aniket", "surname": "jayateerth", "age": 31}
        r = requests.post(self.url, data=payload)
        self.printResult(r, set([200, 201, 204]))

        console.print('[red]Testing file upload')
        payload = {"name": "aniket", "surname": "jayateerth", "age": 31}
        files = {
            'test': open(str(pathlib.Path().absolute()) + '/../test.py', 'rb')
        }
        r = requests.post(self.url, data=payload, files=files)
        self.printResult(r, set([200, 201, 204]))

    def TestPut(self):
        path = str(pathlib.Path().absolute()) + '/../test.py'
        file = open(path, 'rb')
        r = requests.put(self.url + 'test.py', files={'test.py': file})
        self.printResult(r, set([200, 201, 204]))


if __name__ == "__main__":
    Tester = UnitTest()
    console = Console()
    # if options == []:
    #     Tester.TestGET()
    #     Tester.TestHEAD()
    for i in options:
        if (i == '-g'):
            console.print('[cyan]Testing GET method')
            Tester.TestGET()
        if (i == '-cg'):
            console.print('[cyan]Testing Conditional GET method')
            Tester.TestConditionalGET()
        if (i == '-q'):
            console.print('[cyan]Testing Q method')
            Tester.TestQ()
        if (i == '-m'):
            console.print('[cyan]Testing Multiple Methods')
            Tester.TestMultipleMethods()
        if (i == '-h'):
            console.print('[cyan]Testing Head Method')
            Tester.TestHEAD()
        if (i == '-d'):
            console.print('[cyan]Testing Delete Method')
            Tester.TESTdelete()
        if (i == '-p'):
            console.print('[cyan]Testing Post Method')
            Tester.TestPost()
        if (i == '-pt'):
            console.print('[cyan]Testing Put Method')
            Tester.TestPut()
        # if(i == '-gocrazy'):
        #     console.print('[red]Do a random test to crash this server :) ')
        #     Tester.TestMega()
