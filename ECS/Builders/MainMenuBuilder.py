import pygame
from ECS import Factories
from Globals import Settings


class MainMenuBuilder:
    # Define constants
    padding = Settings.MAINMENU_LAYOUT.PADDING
    w, h = (
        Settings.MAINMENU_LAYOUT.USERNAMES_BUTTON_WIDTH,
        Settings.MAINMENU_LAYOUT.USERNAMES_BUTTON_HEIGHT,
    )
    connected_users_btn_ids = []

    @classmethod
    def build(cls, ui: dict, roster: dict):
        # Create Rects
        username_textbox_rect = pygame.Rect(cls.padding, cls.padding, cls.w, cls.h)

        # Define Elements
        cls.username_textbox_id = Factories.create_textbox(
            ui, username_textbox_rect, "Your Username", action="edit_text"
        )

        cls.add_connected_users(ui, roster)

    @classmethod
    def add_connected_users(cls, ui: dict, roster: dict):
        y = cls.h + cls.padding * 2
        for username in roster.values():
            btn_rect = pygame.Rect(cls.padding, y, cls.w, cls.h)

            btn_id = Factories.create_button(ui, btn_rect, username, action="enter_dm")

            cls.connected_users_btn_ids.append(btn_id)

            y += cls.h + cls.padding

    @classmethod
    def update_connected_users(cls, ui: dict, roster: dict):
        for btn_id in cls.connected_users_btn_ids:
            del ui[btn_id]

        cls.connected_users_btn_ids = []

        cls.add_connected_users(ui, roster)

    @classmethod
    def destroy(cls, ui):
        del ui[cls.username_textbox_id]
