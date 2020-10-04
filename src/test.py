documentRoot = ''

def parse_GET_Request(headers):
    # TODO
    # Implement Conditional Get
    # Implement Range Header
    # MIME Encoding response 
    params = {}
    for i in headers[1:]:
        headerField = i[:i.index(':')] 
        params[headerField] = i[i.index(':') + 2 : len(i) - 1]

    print(params)
    path = headers[0].split(' ')[1]
    path = documentRoot + path
    # print(path)
    try:
        if(path == "/"):
            path = 'index.html'
        f = open(path,"r")
        print("OK")
        return "200" #Proper data encoding and sending as a HTTP response
    except FileNotFoundError:
        print("NOT OK")
        return "404" #Change to proper HTTP response


f = open("req.txt","r")
headers = f.readlines()
parse_GET_Request(headers)