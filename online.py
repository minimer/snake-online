import socket


def IPs():
    return [i[-1][0] for i in socket.getaddrinfo(socket.gethostname(), 0, socket.AF_INET)]


class Server:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, int(port)))

    def send(self, data, to):
        data = data.encode('utf-8')
        self.sock.sendto(data, to)

    def get(self):
        data, addres = self.sock.recvfrom(1024)
        return data.decode('utf-8'), addres


class Client:
    def __init__(self, server):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = server
        self.sock.bind(('', 0))

    def send(self, data):
        data = data.encode('utf-8')
        self.sock.sendto(data, self.server)

    def get(self):
        data = self.sock.recv(1024)
        return data.decode('utf-8')