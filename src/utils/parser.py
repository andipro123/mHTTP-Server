class Parser:
    def __init__(self):
        pass

    def parse_headers(data, method):
        if method == 'POST':
            params = {}
            body = []
            boundary = ''

            for line in data[1:]:

                if ':' in line:
                    headerField = line[:line.index(':')]
                    params[headerField] = line[line.index(':') + 2:len(line) -
                                               1]
                elif 'boundary' in line:
                    boundary = line[-1:line.index('=') + 1]

                elif '--' + boundary in line:
                    i = data.index(line)
                    body = data[i:]
                    return (params, body)

                else:
                    if line != '\r' and line != '\n':
                        body.append(line)

            return (params, body)

        elif method == 'PUT':
            params = {}
            body = []
            for line in data[1:]:

                if ':' in line:
                    headerField = line[:line.index(':')]
                    params[headerField] = line[line.index(':') + 2:len(line) -
                                               1]
                else:
                    params['index'] = data.index(line) + 1
                    return (params, body)

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
                # print(boundary)
                for line in body[1:]:
                    if '----' in line:
                        form_data[key] = value
                        key = ''
                        value = ''
                    elif 'Content-Disposition: form-data' in line:
                        if 'filename=' in line:
                            form_data['isFile'] = True
                            filename = line[line.index('ename="') + 7:-2]
                            x = data.index(line)
                            header_string = "\n".join(data[:x + 2])
                            form_data['header_length'] = len(header_string)
                            if filename != "":
                                form_data['filename'] = filename
                        key = line[line.index('=') + 2:-2]
                        value = body[body.index(line) + 2][:-1]

                    elif 'Content-Type' in line or 'filename' in line:
                        file_type = line[line.index(':') + 1:]
                        form_data['file_type'] = file_type
                        form_data['isFile'] = True
                        x = data.index(line)
                        header_string = "\n".join(data[:x + 2])
                        form_data['header_length'] = len(header_string)

                    else:
                        pass

            return form_data

    def parse_url_params(header):

        form_data = {}

        url = header.split(' ')[1]
        string = url[2:].split('&')
        for param in string:
            param = param.split('=')
            form_data[param[0]] = param[1]

        return form_data
