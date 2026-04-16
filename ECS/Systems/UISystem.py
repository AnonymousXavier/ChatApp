from ECS.Builders.MainMenuBuilder import MainMenuBuilder
from ECS.Components import EditTextComponent, TextComponent
from ECS.Systems import NetworkSystem
from ECS.Systems.ChatClient import ChatClient
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

    frame += 1
