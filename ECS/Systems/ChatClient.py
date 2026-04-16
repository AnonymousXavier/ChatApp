import socket
import threading
import json


class ChatClient:
    def __init__(self, host: str, port: int, username: str):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.connected = False

        # State variables for Pygame to read
        self.roster = {}  # Format: {1: "Xavier", 2: "Jesse Ghost"}
        self.inbox = []  # List of received DM packets

        try:
            self.socket.connect((host, port))
            self.connected = True

            # Send initial join packet
            self.send_packet({"type": "join", "username": self.username})

            # Start the SINGLE background listener thread
            threading.Thread(target=self.receive_loop, daemon=True).start()
            print(f"Connected to lab server at {host}:{port}")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def send_packet(self, packet: dict):
        """Packs a dictionary into JSON with a newline delimiter and sends it."""
        if self.connected:
            try:
                payload = (json.dumps(packet) + "\n").encode()
                self.socket.sendall(payload)
            except:
                self.connected = False

    def send_dm(self, target_id: int, text: str):
        """Helper function to format a DM."""
        self.send_packet({"type": "dm", "target_id": target_id, "message": text})

    def update_username(self, new_name: str):
        """Call this from Pygame when the user changes their name in the UI."""
        self.username = new_name
        self.send_packet({"type": "join", "username": self.username})

    def receive_loop(self):
        buffer = ""
        i = 0
        while self.connected:
            try:
                data = self.socket.recv(1024)
                if not data:
                    self.connected = False
                    break

                buffer += data.decode()
                while "\n" in buffer:
                    raw_msg, buffer = buffer.split("\n", 1)
                    packet = json.loads(raw_msg)

                    # --- STATE UPDATE LOGIC ---
                    if packet["type"] == "roster":
                        # Convert string keys back to integers (JSON stringifies dict keys)
                        self.roster = {int(k): v for k, v in packet["users"].items()}

                    elif packet["type"] == "dm":
                        # Add the message to the inbox for Pygame to render
                        self.inbox.append(packet)

            except Exception as err:
                print(err)
                self.connected = False
                break
            i += 1
