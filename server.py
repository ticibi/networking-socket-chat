from datetime import datetime
import socket
import threading
import logging

from config import LOCALHOST, PORT, BUFFER

logging.basicConfig(level=logging.DEBUG)


class Server:
    def __init__(self):
        self.clients = []
        self.usernames = []
        self.max_connections = 5
        self.server_name = 'COOL SERVER'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((LOCALHOST, PORT))
        self.socket.listen()
        logging.debug('[server] ONLINE')
        logging.debug(f'[time] {datetime.utcnow()}')

    def receive(self):
        while True:
            conn, addr = self.socket.accept()
            conn.send(self.server_name.encode())
            username = conn.recv(BUFFER).decode()
            self.clients.append(conn)
            self.usernames.append(username)
            logging.debug(f'[server] received connection from {conn}')
            self.broadcast_message(conn, f'[server] {username} connected')
            thread = threading.Thread(target=self.handle_connection, args=(conn,))
            thread.start()

    def handle_connection(self, conn):
        while True:
            try:
                message = conn.recv(BUFFER)
                self.broadcast_message(conn, f'[{self.usernames[self.clients.index(conn)]}] {message}')
            except Exception:
                self.broadcast_message(conn, f'{self.usernames[self.clients.index(conn)]} disconnected')
                self.usernames.remove(self.usernames[self.clients.index(conn)])
                conn.close()
                self.clients.remove(conn)
                break

    def broadcast_message(self, conn, message):
        logging.debug(message)
        for client in self.clients:
            if client != conn:
                client.send(message.encode())

server = Server()
server.receive()
