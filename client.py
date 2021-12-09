import socket
import threading
import logging

from config import LOCALHOST, PORT, BUFFER

logging.basicConfig(level=logging.DEBUG)


class Client:
    def __init__(self, username=None):
        self.permissions = []
        self.username = username
        if not self.username:
            self.username = input('enter username: ')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((LOCALHOST, PORT))
        self.socket.send(self.username.encode())
        server_name = self.socket.recv(BUFFER).decode()
        logging.debug('connected to', server_name)

    def receive(self):
        while True:
            try:
                incoming = self.socket.recv(BUFFER).decode()
                if incoming:
                    print(incoming)
            except Exception:
                logging.debug('disconnected')
                self.socket.close()
                break
            
    def send(self):
        while True:
            try:
                message = input()
                self.socket.send(message.encode())
            except Exception:
                logging.debug('disconnected')
                self.socket.close()
                break

    def main(self):
        recv_thread = threading.Thread(target=self.receive)
        recv_thread.start()
        send_thread = threading.Thread(target=self.send)
        send_thread.start()

client = Client()
client.main()
