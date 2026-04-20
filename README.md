# ChatApp

A lightweight, peer-to-peer Local Area Network (LAN) chat application built in Python. Instead of relying on traditional GUI libraries, this project utilizes `pygame-ce` to render a completely custom UI framework driven by an Entity-Component-System (ECS) architecture.

## ✨ Features

* **Custom ECS UI Framework:** Built entirely from scratch, featuring dynamic text wrapping, scrollable containers, hover states, and click event handling.
* **LAN Connectivity:** Uses standard Python TCP sockets for fast, reliable local network communication.
* **Auto-Host Node:** The application intelligently detects if a local server is running. If no server is found, it automatically spins up a background host node before connecting as a client.
* **Direct Messaging:** Private peer-to-peer messaging with dynamic roster updates and active connection tracking.
* **Asynchronous Networking:** Utilizes threading to handle background receive loops without blocking or interrupting the UI rendering thread.

## 🛠️ Architecture

The codebase is strictly organized around the **Entity-Component-System** paradigm to cleanly separate state from logic:
* **Components (`ECS/Components.py`):** Pure data structures defining entity attributes (e.g., `TextComponent`, `SpatialComponent`, `ScrollableContainerComponent`).
* **Systems (`ECS/Systems/`):** Logic handlers that process entities possessing specific components (e.g., `RenderingSystem`, `ScrollingSystem`, `NetworkSystem`, `ChatClient`, `ChatServer`).
* **Builders & Factories:** Modular UI construction pipelines (`MainMenuBuilder`, `ChatMenuBuilder`) designed to easily instantiate complex interface layouts.

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed. The only external dependency required is the Pygame Community Edition (CE) library.

```bash
pip install -r requirements.txt
```

### Running the App
Execute the main entry point to launch the application:
```bash
python main.py
```
*Note: The first client to run the application on the local network will automatically host the server on port `55019`. Additionally, the host must update their username at least once to broadcast their identity to other users on the network.*

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details. The software is provided "as is", without warranty of any kind, and the authors or copyright holders are not liable for any claims or damages.
