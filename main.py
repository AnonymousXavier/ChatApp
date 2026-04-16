import pygame

from ECS.Builders.MainMenuBuilder import MainMenuBuilder
from ECS.Systems import (
    InputSystem,
    NetworkSystem,
    RenderingSystem,
    HoveringSystem,
    ClickingSystem,
    UISystem,
)
from Globals import Settings, States


class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        NetworkSystem.init("___")
        MainMenuBuilder.build(States.UI, NetworkSystem.client.roster)

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        RenderingSystem.process(States.UI, self.window)

        pygame.display.update()

    def update(self):
        events = []

        InputSystem.process(States.UI)
        NetworkSystem.process()
        match States.CURRENT_STATE:
            case "MAIN_MENU":
                MainMenuBuilder.update_connected_users(
                    States.UI, NetworkSystem.client.roster
                )

        HoveringSystem.process(States.UI)
        ClickingSystem.process(States.UI, events)
        UISystem.process(States.UI, events)

    def run(self):
        while States.RUNNING:
            self.update()
            self.draw()


Main().run()
