import socket
import threading
import json

from ECS.Systems import TextEditingSystem
from Globals import Settings


class ChatClient:
    def __init__(self, host: str, port: int, username: str):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id_on_server: int = -1
        self.username = username
        self.connected = False

        # State variables for Pygame to read
        self.roster = {}  # Format: {1: "Xavier", 2: "Jesse Ghost"}
        self.inbox = {}  # received Messages
        self.message_indexs = {}  # Helps keep track of the order messages were sent
        self.outbox = {}  # Sent Messages
        self.currently_messageing: int = -1

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

    def send_dm(self, target_id: int, msg: str):
        """Helper function to format a DM."""

        # The message recieved is wrapped perfectly for the textbox
        # Thus we need to re_wrap to the messageboxes size!
        msg = TextEditingSystem.word_wrap(
            msg,
            Settings.CHATMENU_LAYOUT.FONT_SIZE,
            Settings.CHATMENU_LAYOUT.TEXTBOX_WIDTH,
        )

        # Add the message to the outbox
        self.update_messages_dict(
            msg_dict=self.outbox,
            target_id=target_id,
            msg=msg,
        )

        self.send_packet(
            {
                "type": "dm",
                "target_id": target_id,
                "message": msg,
                "sender_id": self.id_on_server,
            },
        )

    def update_username(self, new_name: str):
        """Call this from Pygame when the user changes their name in the UI."""
        self.username = new_name
        self.send_packet({"type": "change_username", "username": self.username})

    def update_messages_dict(self, msg_dict: dict, target_id: int, msg: str):
        if target_id not in msg_dict:
            msg_dict[target_id] = {}

        if target_id not in self.message_indexs:
            self.message_indexs[target_id] = 1

        msg_id = self.message_indexs[target_id]
        msg_dict[target_id][msg_id] = msg

        self.message_indexs[target_id] += 1

    def get_msg_list(self, msg_dict: dict, target_id: int):
        if target_id not in msg_dict:
            msg_dict[target_id] = {}

        return msg_dict[target_id]

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
                        self.roster = {
                            int(client_id): username
                            for client_id, username in packet["users"].items()
                            if int(client_id) != int(self.id_on_server)
                        }

                    elif packet["type"] == "dm":
                        # Add the message to the inbox

                        # Before saving make sure it isnt the message we set
                        if packet["sender_id"] != self.id_on_server:
                            self.update_messages_dict(
                                msg_dict=self.inbox,
                                target_id=packet["sender_id"],
                                msg=packet["message"],
                            )

                    elif packet["type"] == "join":
                        self.id_on_server = int(packet["id"])

            except Exception as _:
                self.connected = False
                break
            i += 1
