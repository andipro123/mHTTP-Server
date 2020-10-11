def parse_headers(data):

    params = {}
    body = []

    for line in data[1:]:

        if ':' in line:
            headerField = line[:line.index(':')]
            params[headerField] = line[line.index(':') + 2:len(line) - 1]

        elif '------' in line:
            i = data.index(line)
            body = data[i:]
            return (params, body)

        else:
            if line != '\r' and line != '\n':
                body.append(line)

    return (params, body)


def parse_body(enctype, body):

    form_data = {}

    if "application/x-www-form-urlencoded" in enctype:
        print(body)
        for line in body:
            line = line.split('&')
            for param in line:
                param = param.split('=')
                form_data[param[0]] = param[1]

    elif "multipart/form-data" in enctype:
        boundary = enctype[enctype.find("=") + 1:]
        key = ''
        value = ''
        print(boundary)
        for line in body[1:]:

            if '----' in line:
                form_data[key] = value
                key = ''
                value = ''
            elif 'Content-Disposition: form-data' in line:
                key = line[line.index('=') + 2:-2]
                value = body[body.index(line) + 2][:-1]

            else:
                pass


# ----WebKitFormBoundarySv3nVnTn1MpFWg2P
# ------WebKitFormBoundarySv3nVnTn1MpFWg2P\r
    print(form_data)
    return form_data
