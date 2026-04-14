import pygame

from ECS.Components import TextComponent


def process(ui: dict, event):
    for element in ui.values():
        if event.key == pygame.K_BACKSPACE:
            if TextComponent not in element:
                continue

            text = element[TextComponent].text
            if text != "":
                element[TextComponent].text = "".join(
                    [text[i] for i in range(len(text) - 1)]
                )
                print(f"Edited: {text} to {element[TextComponent].text}")
            else:
                element[TextComponent].text = ""
                break
            print(event)
        else:
            element[TextComponent].text += event.unicode
