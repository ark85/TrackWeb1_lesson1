# -*- coding: utf-8 -*-
import socket
import datetime
import os

response_headers = {"Server": "py_http_server",
                    "Connection": "close", "Content-Type": "text/html; encoding=utf8"}

def get_response(request):
    if len(request) == 0:
        return response_formation(404, "Not found", "Page not found")
    url = request.splitlines()[0].split()[1]
    headers = {header:content for header,content in (line.split(': ')
                                                     for line in request.rstrip().split("\r\n")[1:])}

    date_time = datetime.datetime.now()
    response_headers["Date"] = date_time.strftime("%a, %d %b %Y %X %Z")

    if url == "/":
        response_body = "<html><head><title>Hello</title></head><body>" + \
                        "Hello mister!\nYou are: " + headers["User-Agent"] + \
                        "</body></html>"
        return response_formation(200, "OK", response_body)
    elif url.startswith("/media"):
        if url == "/media/" or url == "/media":
            dir_content = os.listdir("./files")
            response_body = "<html><head><title>Hello</title></head><body>" + \
                            "".join(["<p><a href='/media/" + file + "'>" + file + "</a></p>\n" for file
                                     in dir_content]) + \
                            "</body></html>"
            return response_formation(200, "OK", response_body)
        else:
            # url[7:] --- without "/media/"
            if url[7:] in os.listdir("./files"):
                file = open("./files/" + url[7:], 'r')
                response_body = "<html><head><title>Hello</title></head><body>" + \
                                file.read() + \
                                "</body></html>"
                file.close()
                return response_formation(200, "OK", response_body)
            else:
                response_body = "<html><head><title>Error not found</title></head><body>" + \
                                "Page not found" + \
                                "</body></html>"
                return response_formation(404, "Not found", response_body)
    elif url == "/test/" or url == "/test":
        response_body = "<html><head><title>Test</title></head><body>" + \
                        request + \
                        "</body></html>"
        return response_formation(200, "OK", response_body)
    else:
        response_body = "<html><head><title>Error not found</title></head><body>" + \
                        "Page not found" + \
                        "</body></html>"
        return response_formation(404, "Not found", response_body)

def response_formation(code, message, response_body):
    response_headers["Content-Length"] = len(response_body)
    response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in \
                                   response_headers.iteritems())
    return "HTTP/1.1 " + str(code) + " " + message + "\n" + response_headers_raw + "\n" + response_body

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # bind socket with host and port
server_socket.listen(0)  # start listening mode for this socket

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # gets the socket’s own address: host and port
        request_string = client_socket.recv(2048)  # receive data from the socket, max amount of data --- 2048 bytes
        client_socket.send(get_response(request_string))  # send response to client
        client_socket.close()
    except KeyboardInterrupt:  # interruption by keyboard (example, ctrl + C)
        print 'Stopped'
        server_socket.close()  # close connection
        exit()
