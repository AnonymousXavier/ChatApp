import socket
import threading
import json


class ChatServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Routing table: {socket_object: {"id": int, "username": str}}
        self.clients = {}
        self.next_id = 1

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"[SERVER] listening on {self.host}:{self.port}")

        # Accept connections in an infinite loop
        while True:
            conn, addr = self.server_socket.accept()

            # Assign ID upon connection, NOT upon receiving a message
            client_id = self.next_id
            self.next_id += 1
            self.clients[conn] = {"id": client_id, "username": f"User_{client_id}"}
            print(f"[SERVER] Connection established: {addr} assigned ID {client_id}")

            # Spawn a dedicated listener for this user
            threading.Thread(
                target=self.handle_client, args=(conn, client_id), daemon=True
            ).start()

    def broadcast_roster(self, sender_socket=None):
        """Builds a dictionary of ID -> Username and blasts it to everyone."""
        roster = {info["id"]: info["username"] for info in self.clients.values()}
        packet = {"type": "roster", "users": roster}
        self.broadcast(packet, sender_socket)

    def broadcast_to(self, specific_socker, data_dict: dict):
        try:
            payload = (json.dumps(data_dict) + "\n").encode()
            specific_socker.send(payload)
        except Exception as err:
            print(err)
            return

    def broadcast(self, data_dict: dict, sender_socket=None):
        """Sends a JSON packet to all connected sockets."""
        payload = (json.dumps(data_dict) + "\n").encode()
        for client_socket in list(self.clients.keys()):
            if client_socket == sender_socket:
                continue
            try:
                client_socket.sendall(payload)
            except Exception as _:
                self.disconnect_client(client_socket)

    def route_direct_message(self, target_id: int, packet: dict):
        """Finds the specific socket holding the target_id and sends the packet."""
        payload = (json.dumps(packet) + "\n").encode()
        for client_socket, info in self.clients.items():
            # Send to everyone (so they even the sender see the message)
            if info["id"] == target_id or info["id"] == packet["sender_id"]:
                try:
                    client_socket.sendall(payload)
                except Exception as err:
                    print(err)
                    self.disconnect_client(client_socket)

    def disconnect_client(self, conn: socket.socket):
        if conn in self.clients:
            print(f"[SERVER] Disconnecting ID {self.clients[conn]['id']}")
            del self.clients[conn]
            conn.close()
            self.broadcast_roster()  # Update everyone else

    def handle_client(self, conn: socket.socket, client_id: int):
        buffer = ""

        # Let Clients Know Their ID so they know what thier roster should look like
        self.broadcast_to(conn, {"type": "join", "id": client_id})

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break

                buffer += data.decode()
                while "\n" in buffer:
                    raw_msg, buffer = buffer.split("\n", 1)
                    packet = json.loads(raw_msg)

                    sender_id = self.clients[conn]["id"]

                    # --- ROUTING LOGIC ---
                    if packet["type"] in ["join", "change_username"]:
                        # Update the username in the routing table, then update everyone
                        self.clients[conn]["username"] = packet["username"]
                        self.broadcast_roster(conn)
                    elif packet["type"] == "dm":
                        # Inject the sender's ID so the receiver knows who it's from
                        packet["sender_id"] = sender_id
                        self.route_direct_message(packet["target_id"], packet)

            except Exception as _:
                break

        self.disconnect_client(conn)


# If running this file directly to host the server:
if __name__ == "__main__":
    host_ip = socket.gethostbyname(socket.gethostname())
    server = ChatServer(host_ip, 55019)
    server.start()
