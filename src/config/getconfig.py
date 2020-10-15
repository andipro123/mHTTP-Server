def getconfig():
    f = open("mhttp.conf","r")
    res = f.read()
    config = {}
    lines = res.split('\n')
    for i in lines:
        try: 
            config[i.split(" ")[0]] = i.split(" ")[1]
        except:
            pass
    return config
