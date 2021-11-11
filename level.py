import pygame as pg


class Level(pg.surface.Surface):
    def __init__(self, name, background):
        super().__init__()
        self.name = name
        self.background = background

