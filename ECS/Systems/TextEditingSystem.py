import pygame

from ECS.Components import EditTextComponent, TextComponent


def process(ui: dict, event):
    for element in ui.values():
        if TextComponent not in element or EditTextComponent not in element:
            continue
        if not element[EditTextComponent].editing:
            continue

        if event.key == pygame.K_BACKSPACE:
            text = element[TextComponent].text
            if text != "":
                element[TextComponent].text = "".join(
                    [text[i] for i in range(len(text) - 1)]
                )
            else:
                element[TextComponent].text = ""
                break
        else:
            element[TextComponent].text += event.unicode
