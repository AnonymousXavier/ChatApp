import pygame
from ECS.Components import (
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
    }

    ui[States.NEXT_UI_ELEMENT_ID] = button
    States.NEXT_UI_ELEMENT_ID += 1
    return new_id


def create_label(ui: dict, rect: pygame.Rect, text: str, font_size: int = 16):
    new_id = States.NEXT_UI_ELEMENT_ID
    button = {
        SpatialComponent: SpatialComponent(rect=rect),
        RenderComponent: RenderComponent(color=Settings.BUTTON.NORMAL_COLOR),
        TextComponent: TextComponent(
            text=text,
            font_size=font_size,
            color=Settings.BUTTON.TEXT_COLOR,
            word_wrap=True,
        ),
    }

    ui[States.NEXT_UI_ELEMENT_ID] = button
    States.NEXT_UI_ELEMENT_ID += 1
    return new_id


def create_textbox(
    ui: dict,
    rect: pygame.Rect,
    text: str,
    action: str,
    font_size: int = 16,
    word_wrap=True,
):
    new_id = States.NEXT_UI_ELEMENT_ID
    button = {
        SpatialComponent: SpatialComponent(rect=rect),
        RenderComponent: RenderComponent(color=Settings.BUTTON.NORMAL_COLOR),
        TextComponent: TextComponent(
            text=text,
            color=Settings.BUTTON.TEXT_COLOR,
            font_size=font_size,
            word_wrap=word_wrap,
        ),
        ClickComponent: ClickComponent(action=action),
        HoverComponent: HoverComponent(
            hovered_color=Settings.BUTTON.HOVER_COLOR,
            normal_color=Settings.BUTTON.NORMAL_COLOR,
        ),
        EditTextComponent: EditTextComponent(),
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
