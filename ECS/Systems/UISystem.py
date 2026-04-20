import time

from ECS.Builders.ChatMenuBuilder import ChatMenuBuilder
from ECS.Builders.MainMenuBuilder import MainMenuBuilder
from ECS.Components import ClickComponent, EditTextComponent, TextComponent
from ECS.Systems import NetworkSystem
from Globals import States

frame = 0


def process(ui: dict, events: list):
    global frame

    # Broadcast Username Change
    if frame % 30 == 0:
        if States.CURRENT_STATE == "MAIN_MENU":
            if ui[MainMenuBuilder.username_textbox_id][EditTextComponent].editing:
                NetworkSystem.client.update_username(
                    ui[MainMenuBuilder.username_textbox_id][TextComponent].text
                )
                frame = 0

    for event in events:
        match event["type"]:
            case "click":
                if event["action"] == "edit_text":
                    ui[event["id"]][EditTextComponent].editing = True
                elif event["action"] == "enter_dm":
                    States.CURRENT_STATE = "CHAT_MENU"
                    # Snuck sm data out of the component.. my bad :(
                    button_id = event["id"]
                    # Button contains the client id
                    extra_data = ui[button_id][ClickComponent].extra_data
                    client_id = extra_data["id"]

                    NetworkSystem.client.currently_messageing = client_id
                elif event["action"] == "send_dm":
                    client_id = NetworkSystem.client.currently_messageing
                    msg = ui[ChatMenuBuilder.chatting_textbox_id][TextComponent].text
                    NetworkSystem.client.send_dm(client_id, msg)

                    time.sleep(1)  # Delay a bit

    frame += 1
