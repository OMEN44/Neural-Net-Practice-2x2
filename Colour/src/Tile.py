import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, colour, size, pos):
        super().__init__()
        self.colourIndex = colour[0]
        self.surf = pygame.surface.Surface(size)
        self.rect = self.surf.get_rect()
        rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.topleft = pos
        pygame.draw.rect(self.surf, colour, rect)

    def updateEvent(self, events):
        pass

    def updateColour(self, colour):
        pygame.draw.rect(self.surf, colour, self.rect)
