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
    send_section_height = h // 2

    chat_labels_id = []

    @classmethod
    def build(cls, ui: dict, person_chatting_with: str):
        # Create Rects
        title_rect = pygame.Rect(cls.padding, cls.padding, cls.w, cls.h)
        send_btn_rect = pygame.Rect(
            cls.padding, cls.padding, cls.send_section_height, cls.send_section_height
        )
        textbox_rect = pygame.Rect(
            cls.padding,
            cls.padding,
            cls.w - cls.padding - send_btn_rect.width,
            cls.send_section_height,
        )
        textbox_rect.bottomleft = (cls.padding, Settings.WINDOW.HEIGHT - cls.padding)

        send_btn_rect.bottomright = (
            Settings.WINDOW.WIDTH - cls.padding,
            Settings.WINDOW.HEIGHT - cls.padding,
        )

        # Define Elements
        cls.person_chatting_with_label_id = Factories.create_label(
            ui, title_rect, person_chatting_with
        )

        cls.chatting_textbox_id = Factories.create_textbox(
            ui, textbox_rect, "Type Something", "edit_text"
        )

        cls.chatting_send_btn_id = Factories.create_button(
            ui, send_btn_rect, ">", "send_dm"
        )

    @classmethod
    def remove_msg_boxes(cls, ui: dict):
        for label_id in cls.chat_labels_id:
            del ui[label_id]

        cls.chat_labels_id = []

    @classmethod
    def add_msg_boxes(cls, ui: dict, inbox: dict, outbox: dict, messages_count: int):
        y = cls.padding * 2 + cls.h

        for i in range(messages_count):
            # determine who sent it
            msg = ""
            if i in inbox:  # Is a recieved message
                msg = inbox[i]
            elif i in outbox:
                msg = outbox[i]

            rect = pygame.Rect(cls.padding, y, cls.w, cls.h)
            cls.chat_labels_id.append(Factories.create_label(ui, rect, msg))

            y += cls.padding + cls.h

    @classmethod
    def update(cls, ui: dict, inbox: dict, outbox: dict, messages_count: int):
        cls.remove_msg_boxes(ui)
        cls.add_msg_boxes(ui, inbox, outbox, messages_count)

    @classmethod
    def destroy(cls, ui):
        del ui[cls.person_chatting_with_label_id]
        del ui[cls.chatting_textbox_id]
        del ui[cls.chatting_send_btn_id]

        cls.remove_msg_boxes(ui)
