import socket

class SocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_socket(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.conn, self.addr = self.sock.accept()

    def send_data(self, data):
        self.conn.send(data.encode())

    def receive_data(self):
        data = self.conn.recv(1024)
        return data.decode()

    def close_socket(self):
        self.conn.close()
        self.sock.close()

def main():
    server = SocketServer('192.168.1.101', 9999)
    server.create_socket()
    # server.send_data('Hello')
    while True:
        print(server.receive_data())
    server.close_socket()

if __name__ == '__main__':
    main()