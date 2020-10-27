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


    def TestGET(self):
        url = ['test.pdf', 'test.png', 'test.html','login.html','File', 'test']
        for i in url:
            r = requests.get(self.url + i)
            if(r.status_code == 404):
                self.printResult(r,404)
            else:
                self.printResult(r,200)

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
    Tester.TestGET()