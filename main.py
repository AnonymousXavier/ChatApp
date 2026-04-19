import pygame
from pygame.time import Clock

from ECS.Systems import (
    InputSystem,
    NetworkSystem,
    RenderingSystem,
    HoveringSystem,
    ClickingSystem,
    StateManager,
    UISystem,
)
from Globals import Settings, States


class Main:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)
        self.clock = Clock()
        NetworkSystem.init("___")
        StateManager.init()

    def draw(self):
        self.window.fill(Settings.COLOURS.BLACK)
        RenderingSystem.process(States.UI, self.window)

        pygame.display.update()

    def update(self):
        dt = self.clock.tick(60) / 1000
        events = []

        print(self.clock.get_fps())

        InputSystem.process(States.UI, dt)
        NetworkSystem.process()
        StateManager.update()

        HoveringSystem.process(States.UI)
        ClickingSystem.process(States.UI, events)
        UISystem.process(States.UI, events)

    def run(self):
        while States.RUNNING:
            self.update()
            self.draw()


Main().run()
