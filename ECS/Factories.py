import pygame
from ECS.Components import (
    BorderComponent,
    ClickComponent,
    HoverComponent,
    RenderComponent,
    ScrollableContainerComponent,
    TextComponent,
    SpatialComponent,
    EditTextComponent,
)
from Globals import Settings, States


def create_button(
    ui: dict,
    rect: pygame.Rect,
    text: str,
    action: str,
    extra_data={},
    font_size: int = 16,
    border_color=(255, 255, 255),
    border_radius=10,
):
    new_id = States.NEXT_UI_ELEMENT_ID
    button = {
        SpatialComponent: SpatialComponent(rect=rect),
        RenderComponent: RenderComponent(color=Settings.BUTTON.NORMAL_COLOR),
        TextComponent: TextComponent(
            text=text, color=Settings.BUTTON.TEXT_COLOR, font_size=font_size
        ),
        ClickComponent: ClickComponent(action=action, extra_data=extra_data),
        HoverComponent: HoverComponent(
            hovered_color=Settings.BUTTON.HOVER_COLOR,
            normal_color=Settings.BUTTON.NORMAL_COLOR,
        ),
        BorderComponent: BorderComponent(color=border_color, radius=border_radius),
    }

    ui[States.NEXT_UI_ELEMENT_ID] = button
    States.NEXT_UI_ELEMENT_ID += 1
    return new_id


def create_label(
    ui: dict, rect: pygame.Rect, text: str, font_size: int = 16, border_color=None
):
    new_id = States.NEXT_UI_ELEMENT_ID
    label = {
        SpatialComponent: SpatialComponent(rect=rect),
        RenderComponent: RenderComponent(color=Settings.TEXTBOX.NORMAL_COLOR),
        TextComponent: TextComponent(
            text=text,
            font_size=font_size,
            color=Settings.TEXTBOX.TEXT_COLOR,
            word_wrap=True,
        ),
    }

    if border_color:
        label[BorderComponent] = BorderComponent(color=border_color)

    ui[States.NEXT_UI_ELEMENT_ID] = label
    States.NEXT_UI_ELEMENT_ID += 1
    return new_id


def create_textbox(
    ui: dict,
    rect: pygame.Rect,
    text: str,
    action: str,
    font_size: int = 16,
    word_wrap=True,
    border_color=(255, 255, 255),
):
    new_id = States.NEXT_UI_ELEMENT_ID
    button = {
        SpatialComponent: SpatialComponent(rect=rect),
        RenderComponent: RenderComponent(color=Settings.TEXTBOX.NORMAL_COLOR),
        TextComponent: TextComponent(
            text=text,
            color=Settings.TEXTBOX.TEXT_COLOR,
            font_size=font_size,
            word_wrap=word_wrap,
        ),
        ClickComponent: ClickComponent(action=action),
        HoverComponent: HoverComponent(
            hovered_color=Settings.TEXTBOX.HOVER_COLOR,
            normal_color=Settings.TEXTBOX.NORMAL_COLOR,
        ),
        EditTextComponent: EditTextComponent(),
        BorderComponent: BorderComponent(color=border_color),
    }

    ui[new_id] = button
    States.NEXT_UI_ELEMENT_ID += 1
    return new_id


def create_scrollable_container(ui: dict, rect: pygame.Rect):
    new_id = States.NEXT_UI_ELEMENT_ID

    container = {
        ScrollableContainerComponent: ScrollableContainerComponent(
            visible_region=(rect.top, rect.bottom)
        ),
        SpatialComponent: SpatialComponent(rect=rect),
    }

    ui[new_id] = container

    States.NEXT_UI_ELEMENT_ID += 1
    return new_id
