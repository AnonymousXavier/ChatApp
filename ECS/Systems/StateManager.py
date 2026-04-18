from ECS.Builders.ChatMenuBuilder import ChatMenuBuilder
from ECS.Builders.MainMenuBuilder import MainMenuBuilder
from ECS.Systems import NetworkSystem
from Globals import States

last_frames_state: States.STATES_LITERAL = "MAIN_MENU"


def init(new_state=None):
    if not new_state:
        new_state = States.CURRENT_STATE

    match new_state:
        case "MAIN_MENU":
            MainMenuBuilder.build(States.UI, NetworkSystem.client.roster)

            print("Created MainMenu")
        case "CHAT_MENU":
            ChatMenuBuilder.build(
                States.UI,
                NetworkSystem.client.roster[NetworkSystem.client.currently_messageing],
            )

            print("Created ChatMenu")


def update():
    global last_frames_state

    if last_frames_state != States.CURRENT_STATE:
        transition_to_next_state(last_frames_state, States.CURRENT_STATE)

    match States.CURRENT_STATE:
        case "MAIN_MENU":
            MainMenuBuilder.update_connected_users(
                States.UI, NetworkSystem.client.roster
            )
        case "CHAT_MENU":
            target_id = NetworkSystem.client.currently_messageing
            inbox = NetworkSystem.client.inbox
            outbox = NetworkSystem.client.outbox
            msg_indexs = NetworkSystem.client.message_indexs

            ChatMenuBuilder.update(
                States.UI,
                NetworkSystem.client.get_msg_list(inbox, target_id),
                NetworkSystem.client.get_msg_list(outbox, target_id),
                msg_indexs[target_id] if target_id in msg_indexs else 0,
            )

    last_frames_state = States.CURRENT_STATE


def transition_to_next_state(_from: States.STATES_LITERAL, _to: States.STATES_LITERAL):
    match _from:
        case "MAIN_MENU":
            MainMenuBuilder.destroy(States.UI)

            print("Destroyed MainMenu")

        case "CHAT_MENU":
            ChatMenuBuilder.destroy(States.UI)

            print("Destroyed ChatMenu")

    init(_to)
