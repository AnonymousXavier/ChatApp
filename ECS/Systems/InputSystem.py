import pygame

from ECS.Systems import TextEditingSystem
from Globals import States


def process(ui: dict):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            States.RUNNING = False
        if event.type == pygame.KEYDOWN:
            TextEditingSystem.process(ui, event)
