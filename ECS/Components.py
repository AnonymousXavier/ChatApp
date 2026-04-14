import pygame

from dataclasses import dataclass


@dataclass(kw_only=True)
class TextComponent:
    text: str
    font_size: int = (
        16  # I can get away with creating fonts often cos its a simple program
    )
    color: tuple


@dataclass(kw_only=True)
class SpatialComponent:
    rect: pygame.Rect


@dataclass(kw_only=True)
class RenderComponent:
    color: tuple


@dataclass(kw_only=True)
class ClickComponent:
    clicked: bool = False
    action: str


@dataclass(kw_only=True)
class HoverComponent:
    hovered_color: tuple
    normal_color: tuple


@dataclass(kw_only=True)
class EditTextComponent:
    editing: bool = False
