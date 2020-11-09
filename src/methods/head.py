from get import parse_GET_Request


def parse_HEAD_Request(headers, cli):
    # Returns the response of GET without the message body
    # TODO
    return parse_GET_Request(headers, cli, "HEAD")