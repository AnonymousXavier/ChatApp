import pygame
from ECS.Components import HoverComponent, RenderComponent, SpatialComponent


def process(ui: dict):
    for element in ui.values():
        if (
            HoverComponent in element
            and SpatialComponent in element
            and RenderComponent in element
        ):
            mouse_pos = pygame.mouse.get_pos()
            if element[SpatialComponent].rect.collidepoint(mouse_pos):
                element[RenderComponent].color = element[HoverComponent].hovered_color
            else:
                element[RenderComponent].color = element[HoverComponent].normal_color
