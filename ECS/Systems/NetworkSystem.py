import time
import threading
from ECS.Systems.ChatServer import ChatServer
from ECS.Systems.ChatClient import ChatClient

import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 55019
client: ChatClient

frame = 1


def init(username: str):
    global client

    # Try to initialize the client
    client = ChatClient(HOST, PORT, username)

    # If it failed to connect, boot the server in the background and try again
    if not client.connected:
        print("No server detected. Booting Host Node...")
        server = ChatServer(HOST, PORT)
        threading.Thread(target=server.start, daemon=True).start()

        time.sleep(1)  # Delay a bit
        client = ChatClient(HOST, PORT, username)


def process():
    global frame

    if frame % 30 == 0:
        threading.Thread(target=client.receive_loop, daemon=True).start()
    frame += 1
