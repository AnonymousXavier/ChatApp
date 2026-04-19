import pygame

from ECS.Components import ScrollableContainerComponent


def process(ui: dict, event: pygame.Event, dt: float):
    dy = event.y * -1
    scroll_speed = 300 * dt

    for element in ui.values():
        if ScrollableContainerComponent in element:
            t, b = element[ScrollableContainerComponent].visible_region
            t, b = t + dy * scroll_speed, b + dy * scroll_speed

            element[ScrollableContainerComponent].visible_region = t, b
