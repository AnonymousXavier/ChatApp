import time
import threading
from ECS.Systems.ChatServer import ChatServer
from ECS.Systems.ChatClient import ChatClient

import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 55019

# 1. Try to initialize the client
client = ChatClient(HOST, PORT, "Xavier")

# 2. If it failed to connect, boot the server in the background and try again
if not client.connected:
    print("No server detected. Booting Host Node...")
    server = ChatServer(HOST, PORT)
    threading.Thread(target=server.start, daemon=True).start()

    time.sleep(0.5)  # Wait for doors to open
    client = ChatClient(HOST, PORT, "Xavier")

# 3. Enter your Pygame loop (Simulated here with console for now)
# Inside your Pygame ECS, you just read `client.roster` to draw the menu buttons
# and read `client.inbox` to draw the chat history.

while client.connected:
    # Pygame would do this via UI, we'll do it via console for testing:
    print(f"\n--- MAIN MENU ---")
    print(f"Online Users: {client.roster}")

    target_str = input("Enter the ID of the user to message (or 'quit'): ")
    if target_str == "quit":
        break

    msg = input("Enter your message: ")
    client.send_dm(int(target_str), msg)

    # Wait a tiny bit for the server to route it back to us, then print inbox
    time.sleep(0.1)
    print(f"\nYour Inbox History: {client.inbox}")
