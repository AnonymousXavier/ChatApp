import pygame
from ECS.Components import EditTextComponent, SpatialComponent, TextComponent
from Globals import Settings

pygame.init()


def calculate_char_width_to_font_size_slope(font_name: str = "Consolas"):
    # Basically lets us use linear interpolation
    # And we can cos it assumes a monospaced font is used

    char = "A"
    upperLimit = 100
    lowerLimit = 10

    w1 = pygame.font.SysFont(font_name, lowerLimit).size(char)[0]
    w2 = pygame.font.SysFont(font_name, upperLimit).size(char)[0]

    char_slope = (w2 - w1) / (upperLimit - lowerLimit)

    # Get the width of spaces
    space_width = w1 - (char_slope * lowerLimit)

    return space_width, char_slope


char_space_width, char_width_font_size_slope = calculate_char_width_to_font_size_slope()


def process(ui: dict, event):
    for element in ui.values():
        if TextComponent not in element or EditTextComponent not in element:
            continue
        if not element[EditTextComponent].editing:
            continue

        if event.key == pygame.K_BACKSPACE:
            text = element[TextComponent].text
            if text != "":
                element[TextComponent].text = remove_last_letter_of(text)
            else:
                element[TextComponent].text = ""
                break
        else:
            element[TextComponent].text += event.unicode

        element[TextComponent].text = word_wrap(
            element[TextComponent], element[SpatialComponent].rect
        )


def remove_last_letter_of(text: str):
    return "".join([text[i] for i in range(len(text) - 1)])


def approx_word_width(char_n: int, font_size: int):
    # Get width of a single char
    char_width = char_width_font_size_slope * font_size
    # Scale it
    return char_width * char_n


# Reverse engineer the word width func
def approx_word_count(width: int, font_size: int, padding: float):
    return (width - (padding * 4)) / (char_width_font_size_slope * font_size)


def word_wrap(TextComponent: TextComponent, rect: pygame.Rect):
    padding = Settings.MAINMENU_LAYOUT.PADDING
    # Determine the optimal characters count
    opt_char_per_line = approx_word_count(rect.width, TextComponent.font_size, padding)

    # Make sure to remove the newlines
    raw_text = TextComponent.text.replace("\n", "")

    # Create the effect
    i = 0
    wrapped_word = ""
    for char in raw_text:
        if i > opt_char_per_line:
            wrapped_word += "\n"
            i = 0
        wrapped_word += char
        i += 1

    return wrapped_word
