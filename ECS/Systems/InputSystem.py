import pygame

from ECS.Systems import ScrollingSystem, TextEditingSystem
from Globals import States


def process(ui: dict, dt: float):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            States.RUNNING = False
        if event.type == pygame.KEYDOWN:
            TextEditingSystem.process(ui, event)

        if event.type == pygame.MOUSEWHEEL:
            ScrollingSystem.process(ui, event, dt)
