import pygame

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class TextComponent:
    text: str
    font_name: str = "Consolas"
    font_size: int = (
        16  # I can get away with creating fonts often cos its a simple program
    )
    color: tuple

    word_wrap: bool = False
    grow_direction: str = "down"


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
    extra_data: dict = field(
        default_factory=dict
    )  # Unfortunately, ill be using this to carry data


@dataclass(kw_only=True)
class HoverComponent:
    hovered_color: tuple
    normal_color: tuple


@dataclass(kw_only=True)
class ScrollableContainerComponent:
    element_ids: list = field(default_factory=list)
    visible_region: tuple  # top, bottom


@dataclass(kw_only=True)
class EditTextComponent:
    editing: bool = False
