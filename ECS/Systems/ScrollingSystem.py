import pygame
from pygame.math import clamp

from ECS.Components import ScrollableContainerComponent, SpatialComponent
from Globals import States


def process(ui: dict, event: pygame.Event, dt: float):
    dy = event.y * -1
    scroll_speed = dt * 100

    for element_id, element in ui.items():
        if ScrollableContainerComponent in element:
            t, b = element[ScrollableContainerComponent].visible_region
            _t, _b = t + dy * scroll_speed, b + dy * scroll_speed

            center_y = (_t + _b) / 2
            container_h = b - t

            # Get height to of container children
            min_y = float("inf")
            max_y = -1

            for child in States.CONTAINERS[element_id].values():
                child_rect = child[SpatialComponent].rect
                if child_rect.bottom > max_y:
                    max_y = child_rect.bottom

                if child_rect.top < min_y:
                    min_y = child_rect.top

            children_cumulative_height = max_y - min_y

            # Only Scroll if theres more to show
            if container_h < children_cumulative_height:
                center_y = clamp(
                    center_y, min_y + container_h / 2, max_y - container_h / 2
                )
                t = center_y - container_h / 2
                b = center_y + container_h / 2

                element[ScrollableContainerComponent].visible_region = t, b
