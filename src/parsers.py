def parse_headers(data):

    params = {}
    body = []

    # print(data)
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


def parse_body(enctype, body, type, data):

    if type == 'POST':
        form_data = {}

        if "application/x-www-form-urlencoded" in enctype:
            # print(body)
            for line in body:
                line = line.split('&')
                for param in line:
                    param = param.split('=')
                    form_data[param[0]] = param[1]

        elif "multipart/form-data" in enctype:
            boundary = enctype[enctype.find("=") + 1:]
            key = ''
            value = ''
            form_data['isFile'] = False
            # print(body)
            # print(boundary)
            for line in body[1:]:
                if '----' in line:
                    form_data[key] = value
                    key = ''
                    value = ''
                elif 'Content-Disposition: form-data' in line:
                    if 'filename=' in line:
                        filename = line[line.index('ename="') + 7:-2]
                        form_data['filename'] = filename
                    key = line[line.index('=') + 2:-2]
                    value = body[body.index(line) + 2][:-1]

                elif 'Content-Type' in line:
                    form_data['isFile'] = True
                    x = data.index(line)
                    header_string = "\n".join(data[:x + 2])
                    # form_data['filedata'] = "\n".join(
                    #     body[body.index(line) + 2:][:-3]) + "\n"

                    form_data['header_length'] = len(header_string)

                    # print(form_data['filedata'].encode('ISO-8859-1'))
                else:
                    pass

            # ----WebKitFormBoundarySv3nVnTn1MpFWg2P
            # ------WebKitFormBoundarySv3nVnTn1MpFWg2P\r
            # print(len(form_data['filedata']))
        return form_data

    elif type == 'PUT':
        form_data = {}
        boundary = enctype[enctype.find("=") + 1:]
        key = ''
        value = ''
        form_data['isFile'] = False

        # print(boundary)
        for line in body[1:]:

            if '----' in line:
                form_data[key] = value
                key = ''
                value = ''
            elif 'Content-Disposition: form-data' in line:
                key = line[line.index('=') + 2:-2]
                value = body[body.index(line) + 2][:-1]

            elif 'Content-Type' in line:
                form_data['isFile'] = True
                x = data.index(line)
                header_string = "\n".join(data[:x + 2])
                # form_data['filedata'] = "\n".join(
                #     body[body.index(line) + 2:][:-3]) + "\n"

                form_data['header_length'] = len(header_string)
            else:
                pass
        # print(form_data)
        return form_data
