import pygame
from ECS.Components import ClickComponent, RenderComponent, SpatialComponent


def process(ui: dict, events: list):
    for element_id, element in ui.items():
        if (
            ClickComponent in element
            and SpatialComponent in element
            and RenderComponent in element
        ):
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = element[SpatialComponent].rect.collidepoint(mouse_pos)
            right_mouse_clicked = pygame.mouse.get_pressed()[0]

            if is_hovered and right_mouse_clicked:
                events.append(
                    {
                        "type": "click",
                        "action": element[ClickComponent].action,
                        "id": element_id,
                    }
                )
                break
