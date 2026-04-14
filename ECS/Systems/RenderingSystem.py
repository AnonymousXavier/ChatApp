import pygame
from ECS.Components import RenderComponent, SpatialComponent, TextComponent

pygame.font.init()


def process(ui: dict, surface: pygame.Surface):
    for _, element in ui.items():
        if SpatialComponent in element and RenderComponent in element:
            pygame.draw.rect(
                surface, element[RenderComponent].color, element[SpatialComponent].rect
            )
            if TextComponent in element:
                font = pygame.font.SysFont(
                    "Courier New", element[TextComponent].font_size
                )
                text_surface = font.render(
                    element[TextComponent].text, True, element[TextComponent].color
                )
                text_rect = text_surface.get_rect(
                    center=element[SpatialComponent].rect.center
                )
                surface.blit(text_surface, text_rect)
