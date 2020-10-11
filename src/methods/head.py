from get import parse_GET_Request
def parse_HEAD_Request(headers):
    # Returns the response of GET without the message body
    # TODO
    # Add more headers to the repsonse in the reponse.py file
    # Handle Caching with GET
    return parse_GET_Request(headers, "HEAD")