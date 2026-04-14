import pygame
from ECS import Factories
from Globals import Settings


class MainMenuBuilder:
    @classmethod
    def build(cls, ui: dict):
        # Define constants
        padding = Settings.MAINMENU_LAYOUT.PADDING
        w, h = (
            Settings.MAINMENU_LAYOUT.USERNAMES_BUTTON_WIDTH,
            Settings.MAINMENU_LAYOUT.USERNAMES_BUTTON_HEIGHT,
        )

        # Create Rects
        username_textbox_rect = pygame.Rect(padding, padding, w, h)

        # Define Elements
        cls.username_textbox_id = Factories.create_textbox(
            ui, username_textbox_rect, "Your Username", action="edit_text"
        )

    @classmethod
    def destroy(cls, ui):
        del ui[cls.username_textbox_id]
