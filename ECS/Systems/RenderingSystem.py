import pygame
from ECS.Components import (
    RenderComponent,
    ScrollableContainerComponent,
    SpatialComponent,
    TextComponent,
)
from Globals import States

pygame.font.init()


def process(ui: dict, surface: pygame.Surface):
    for element_id, element in ui.items():
        if SpatialComponent in element and RenderComponent in element:
            draw_element(
                surface=surface,
                element=element,
                drawn_rect=element[SpatialComponent].rect,
            )
        elif SpatialComponent in element and ScrollableContainerComponent in element:
            if element_id not in States.CONTAINERS:
                continue
            top, bottom = element[ScrollableContainerComponent].visible_region
            container_rect_top = element[SpatialComponent].rect.top
            for container_child in States.CONTAINERS[element_id].values():
                ref_rect: pygame.Rect = container_child[SpatialComponent].rect
                if (
                    ref_rect.y > top or ref_rect.y < bottom
                ):  # So things dont just disapear as we scroll
                    new_rect = pygame.Rect(
                        ref_rect.x,
                        container_rect_top + ref_rect.y - top,
                        ref_rect.w,
                        ref_rect.h,
                    )

                    draw_element(
                        surface=surface, element=container_child, drawn_rect=new_rect
                    )


def draw_element(surface: pygame.Surface, element: dict, drawn_rect: pygame.Rect):
    # Draw Background if text components doesnt have wordwrap
    if TextComponent not in element or not element[TextComponent].word_wrap:
        pygame.draw.rect(
            surface,
            element[RenderComponent].color,
            drawn_rect,
        )
    if TextComponent in element:
        font = pygame.font.SysFont(
            element[TextComponent].font_name, element[TextComponent].font_size
        )

        text_surface = font.render(
            element[TextComponent].text, True, element[TextComponent].color
        )

        text_rect = text_surface.get_rect(center=drawn_rect.center)

        if element[TextComponent].word_wrap:
            grown_rect = text_surface.get_rect()
            grown_rect.width = drawn_rect.width
            grown_rect.height = max(drawn_rect.height, grown_rect.height)

            if element[TextComponent].grow_direction == "down":
                grown_rect.topleft = drawn_rect.topleft
            elif element[TextComponent].grow_direction == "up":
                grown_rect.bottomright = drawn_rect.bottomright

            text_rect.center = grown_rect.center

            pygame.draw.rect(
                surface,
                element[RenderComponent].color,
                grown_rect,
            )

        surface.blit(text_surface, text_rect)
