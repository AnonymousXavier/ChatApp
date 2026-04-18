import pygame
from ECS.Components import (
    ClickComponent,
    HoverComponent,
    RenderComponent,
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
            text=text, font_size=font_size, color=Settings.BUTTON.TEXT_COLOR
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
    grows=False,
):
    new_id = States.NEXT_UI_ELEMENT_ID
    button = {
        SpatialComponent: SpatialComponent(rect=rect),
        RenderComponent: RenderComponent(color=Settings.BUTTON.NORMAL_COLOR),
        TextComponent: TextComponent(
            text=text, color=Settings.BUTTON.TEXT_COLOR, font_size=font_size
        ),
        ClickComponent: ClickComponent(action=action),
        HoverComponent: HoverComponent(
            hovered_color=Settings.BUTTON.HOVER_COLOR,
            normal_color=Settings.BUTTON.NORMAL_COLOR,
        ),
        EditTextComponent: EditTextComponent(grows=grows),
    }

    ui[States.NEXT_UI_ELEMENT_ID] = button
    States.NEXT_UI_ELEMENT_ID += 1
    return new_id
