from typing import Literal

NEXT_UI_ELEMENT_ID = 1
RUNNING = True

STATES_LITERAL = Literal["MAIN_MENU", "CHAT_MENU"]
CURRENT_STATE: STATES_LITERAL = "MAIN_MENU"

UI = {}
CONTAINERS = {}  # Where Containers store elements data [cos they only hold the ids]
