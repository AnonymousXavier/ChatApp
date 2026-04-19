import pygame
from ECS import Factories
from ECS.Components import TextComponent
from Globals import Settings, States

pygame.init()


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

        container_rect = pygame.Rect(
            cls.padding,
            title_rect.bottom + cls.padding,
            title_rect.width,
            textbox_rect.top - title_rect.bottom - cls.padding * 2,
        )

        send_btn_rect.bottomright = (
            Settings.WINDOW.WIDTH - cls.padding,
            Settings.WINDOW.HEIGHT - cls.padding,
        )

        # Define Elements
        # Ensure Chatting Texbox is over messages
        cls.person_chatting_with_label_id = Factories.create_label(
            ui, title_rect, person_chatting_with
        )

        cls.container_id = Factories.create_scrollable_container(ui, container_rect)

        cls.chatting_textbox_id = Factories.create_textbox(
            ui, textbox_rect, "Type Something", "edit_text"
        )

        cls.chatting_send_btn_id = Factories.create_button(
            ui, send_btn_rect, ">", "send_dm"
        )

        ui[cls.chatting_textbox_id][TextComponent].grow_direction = "up"
        ui[cls.chatting_textbox_id][TextComponent].word_wrap = True

        States.CONTAINERS[cls.container_id] = {}

    @classmethod
    def remove_msg_boxes(cls, ui: dict):
        for label_id in cls.chat_labels_id:
            del States.CONTAINERS[cls.container_id][label_id]

        cls.chat_labels_id = []

    @classmethod
    def add_msg_boxes(cls, ui: dict, inbox: dict, outbox: dict, messages_count: int):
        y = cls.padding * 2 + cls.h

        # Estimate the height
        font = pygame.font.SysFont("Consolas", 16)
        h = font.render("O", True, (0, 0, 0)).get_size()[1]
        line_spacing = font.get_descent()

        for i in range(messages_count):
            if i not in inbox and i not in outbox:
                continue

            # determine who sent it
            msg = ""
            rect = pygame.Rect(cls.padding, y, cls.w * 2 / 3, cls.h)

            if i in inbox:  # Is a recieved message
                msg = inbox[i]
                rect.left = cls.padding
            elif i in outbox:  # Is a sent message
                msg = outbox[i]
                rect.right = Settings.WINDOW.WIDTH - cls.padding

            cls.chat_labels_id.append(
                Factories.create_label(States.CONTAINERS[cls.container_id], rect, msg)
            )
            h = pygame.font.SysFont("Consolas", 16).size(msg)[1]

            y += cls.padding + max((h + line_spacing) * (4 + msg.count("\n")), cls.h)

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
