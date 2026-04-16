import pygame
from ECS import Factories
from Globals import Settings


class ChatMenuBuilder:
    # Define constants
    padding = Settings.MAINMENU_LAYOUT.PADDING
    w, h = (
        Settings.MAINMENU_LAYOUT.USERNAMES_BUTTON_WIDTH,
        Settings.MAINMENU_LAYOUT.USERNAMES_BUTTON_HEIGHT,
    )

    chat_labels_id = []

    @classmethod
    def build(cls, ui: dict, roster: dict):
        # Create Rects
        username_textbox_rect = pygame.Rect(cls.padding, cls.padding, cls.w, cls.h)

        # Define Elements
        cls.username_textbox_id = Factories.create_textbox(
            ui, username_textbox_rect, "Your Username", action="edit_text"
        )

    @classmethod
    def add_mssg(cls, ui: dict, inbox: dict, outbox: dict):
        for label_id in cls.chat_labels_id:
            del ui[btn_id]

        cls.connected_users_btn_ids = []

    @classmethod
    def destroy(cls, ui):
        del ui[cls.username_textbox_id]
