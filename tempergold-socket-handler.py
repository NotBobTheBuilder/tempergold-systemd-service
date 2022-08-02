from socket import fromfd
from socketserver import BaseRequestHandler, UnixStreamServer
from sys import argv
from tempergold import read_temperature

class Handler(BaseRequestHandler):
    def handle(self):
        path = '/dev/' + argv[1]
        temp = str(read_temperature(path))
        self.request.sendall(temp.encode('utf-8'))

class SystemDServer(UnixStreamServer):
    def server_bind(self):
        self.socket = fromfd(3, self.address_family, self.socket_type)

with SystemDServer('', Handler) as s:
    s.serve_forever()
