import pygame
from ECS.Components import (
    EditTextComponent,
    RenderComponent,
    SpatialComponent,
    TextComponent,
)

pygame.font.init()


def process(ui: dict, surface: pygame.Surface):
    for _, element in ui.items():
        if SpatialComponent in element and RenderComponent in element:
            pygame.draw.rect(
                surface, element[RenderComponent].color, element[SpatialComponent].rect
            )
            if TextComponent in element:
                font = pygame.font.SysFont(
                    element[TextComponent].font_name, element[TextComponent].font_size
                )

                text_surface = font.render(
                    element[TextComponent].text, True, element[TextComponent].color
                )

                text_rect = text_surface.get_rect(
                    center=element[SpatialComponent].rect.center
                )

                if EditTextComponent not in element:
                    surface.blit(text_surface, text_rect)
                    continue

                if element[EditTextComponent].grows:
                    grown_rect = text_surface.get_rect()
                    grown_rect.width = element[SpatialComponent].rect.width

                    if element[EditTextComponent].grow_direction == "down":
                        grown_rect.topleft = element[SpatialComponent].rect.topleft
                    elif element[EditTextComponent].grow_direction == "up":
                        grown_rect.bottomright = element[
                            SpatialComponent
                        ].rect.bottomright

                    text_rect.center = grown_rect.center

                    pygame.draw.rect(
                        surface,
                        element[RenderComponent].color,
                        grown_rect,
                    )

                surface.blit(text_surface, text_rect)
