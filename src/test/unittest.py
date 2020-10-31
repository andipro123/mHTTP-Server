import requests
import sys
from rich import box
from rich.console import Console
from rich.table import Table

console = Console(highlight=False)




class UnitTest:
    def __init__(self):
        self.port = sys.argv[1]
        self.url = "http://localhost:{}/".format(self.port)
 
    def printResult(self, r, expectedCode):
        table = Table(title="Result",box = box.ASCII)
        table.add_column("Method")
        table.add_column("Response",style="green")
        table.add_column("Message",style="blue")
        table.add_column("Test Result")
        code = r.status_code
        if (code == expectedCode):
            result = '[green]Success'
        else:
            result = '[red]Failed'
        table.add_row(r.request.method,str(r.status_code),r.reason,result)
        console.print(table)


    def MultipleMethods(self):
        # methods = ['get','head','post','put']
        data = {
            'name' : 'UnitTest1.0'
        }
        r = requests.get(self.url)
        self.printResult(r,200)
        r = requests.post(self.url,data = data)
        self.printResult(r,200)
        r = requests.head(self.url)
        self.printResult(r,200)
        # r = requests.put(self.url,data = data)
        # self.printResult(r,200)
        
    
    def TestGET(self):
        url = ['test.pdf', 'test.png', 'test.html','login.html','File', 'test']
        for i in url:
            r = requests.get(self.url + i)
            if(r.status_code == 404):
                self.printResult(r,404)
            else:
                self.printResult(r,200)
            console.print('Body Length: ',len(r.text))
        r = requests.get(self.url, headers = {'Content-Encoding' : 'NotExistent'})
        self.printResult(r,415)
        console.print('Body Length: ',len(r.text))

    
    def TestQ(self):
        #Q parameter to request for specific data types
        #Based on the values mentioned for each type the highest value will be returned if available
        #If no matching value is requested then send 406
        types = {
            'application/pdf' : 0.3,
            'image/png' : 0.4,
            'ai/ai': 1.0
        }
        s = ''
        for k in types.keys():
            s += k + ';q={}'.format(types[k]) + ',' 
        r = requests.get(self.url + 'test', headers = {'Accept' : s})
        console.print('Testing variable accept type according to priority')
        if(r.status_code == 406):
            self.printResult(r,406)
        else:
            self.printResult(r,200)
        console.print('Body Length:', len(r.text))

    def TestHEAD(self):
        url = ['test.pdf', 'test.png', 'test.html','login.html','File', 'test']
        for i in url:
            r = requests.head(self.url + i)
            if(r.status_code == 404):
                self.printResult(r,404)
            else:
                self.printResult(r,200)
            console.print('Body Length: ',len(r.text))

    

    def TestBadAccept(self,Atype = "test/html"):
        r = requests.get(self.url, headers = {'Accept' : Atype})
        self.printResult(r,406)
    # Expected to fetch the Etag from the server and send this in the next request.
    # Returns 304 if the resource is not modified
    # To check either ways send an optional string as Etag and the resource will be sent with 200
    def TestConditionalGET(self, etag = ""):
        url = self.url + "test.pdf"
        console.print("Getting metadata about the resource.")
        r = requests.head(url)
        self.printResult(r,200)
        console.print("Checking if the resource is modified.")
        if(etag == ""):
            try:
                etag = r.headers['E-Tag']
                r = requests.get(url, headers = {'If-None-Match' : etag})
            except:
                return
        else:
            r = requests.get(url, headers = {'If-None-Match' : etag})
        self.printResult(r,304)

if __name__ == "__main__":
    Tester = UnitTest()
    # Tester.TestConditionalGET()
    # Tester.TestBadAccept()
    # Tester.TestHEAD()
    # Tester.TestGET()
    Tester.TestQ()
    # Tester.MultipleMethods()