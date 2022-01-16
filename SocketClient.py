import socket

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_socket(self):
        self.sock.connect((self.host, self.port))

    def send_data(self, data):
        self.sock.send(data.encode())

    def receive_data(self):
        data = self.sock.recv(1024)
        return data.decode()

    def close_socket(self):
        self.sock.close()

def main():
    client = SocketClient('127.0.0.1', 9999)
    client.create_socket()
    client.send_data('Hello')
    print(client.receive_data())
    client.close_socket()

if __name__ == '__main__':
    main()