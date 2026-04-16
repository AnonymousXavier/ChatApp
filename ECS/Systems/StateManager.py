from ECS.Builders.MainMenuBuilder import MainMenuBuilder
from ECS.Systems import NetworkSystem
from Globals import States


def init():
    match States.CURRENT_STATE:
        case "MAIN_MENU":
            MainMenuBuilder.build(States.UI, NetworkSystem.client.roster)
        case "CHAT_MENU":
        	
