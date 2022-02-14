import math
import random
import pygame
import threading

from Colour.src.Tile import Tile
from src.Renderer import render_loop
from src.TileList import TileList


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class Game:

    def __init__(self):

        pygame.init()
        pygame.font.init()
        self.WINDOW_WIDTH = 1024
        self.WINDOW_HEIGHT = 640
        self.FPS = 60
        self.WINDOW_NAME = "Colour Render"

        self.icon = pygame.image.load("icon.jpeg")  # Sets The Icon Image Object
        pygame.display.set_icon(self.icon)

        self.mainClock = pygame.time.Clock()
        self.run = True

        self.font = pygame.font.SysFont("arial", 20)
        self.text = self.font.render("PlaceHolder", True, (0, 0, 0))

        self.surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(self.WINDOW_NAME)
        self.objects = pygame.sprite.Group()
        self.ui = pygame.sprite.Group()
        self.buttons = []
        self.tileList = TileList()
        self.layout()

    def loop(self):
        while self.run:
            self.inputs()
            self.render()
            self.mainClock.tick(self.FPS)
            self.displayFPS()
            self.update()
        pygame.quit()

    def displayFPS(self):
        pygame.display.set_caption(self.WINDOW_NAME + " | " + str(int(self.mainClock.get_fps())))

    def update(self):
        pass

    def inputs(self):
        events = pygame.event.get()
        for object in self.objects:
            object.updateEvent(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.setRandomTile()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for item in self.buttons:
                    item.mouse_click()

    def render(self):
        self.surface.fill((255, 255, 255))
        screensize = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        render_loop(self.ui, self.surface)
        render_loop(self.objects, self.surface)
        render_loop(self.tileList, self.surface)
        self.surface.blit(self.text, (50, 600))
        pygame.display.update()

    def layout(self) -> None:
        self.SIZE = 150
        self.X = self.WINDOW_WIDTH / 2 - self.SIZE
        self.Y = self.WINDOW_HEIGHT / 2 - self.SIZE - 50
        self.setRandomTile()

    def randomColour(self) -> tuple[int, int, int]:
        value = random.randint(0, 255)
        return value, value, value

    def setRandomTile(self) -> None:
        self.tileList.setTile(1, Tile(self.randomColour(), (self.SIZE, self.SIZE), (self.X, self.Y)))
        self.tileList.setTile(2, Tile(self.randomColour(), (self.SIZE, self.SIZE), (self.X + self.SIZE, self.Y)))
        self.tileList.setTile(3, Tile(self.randomColour(), (self.SIZE, self.SIZE), (self.X, self.Y + self.SIZE)))
        self.tileList.setTile(4, Tile(self.randomColour(), (self.SIZE, self.SIZE),
                                      (self.X + self.SIZE, self.Y + self.SIZE)))
        self.genNetworkThread()

    def genNetworkThread(self) -> None:
        thread = threading.Thread(target=self.networkThread)
        thread.start()

    def setText(self, string: str):
        self.text = self.font.render(string, True, (0, 0, 0))

    def setTileColour(self, index, value):
        if index == 1:
            self.tileList.setTile(1, Tile(value, (self.SIZE, self.SIZE), (self.X, self.Y)))
        elif index == 2:
            self.tileList.setTile(2,
                                  Tile(value, (self.SIZE, self.SIZE), (self.X + self.SIZE, self.Y)))
        elif index == 3:
            self.tileList.setTile(3,
                                  Tile(value, (self.SIZE, self.SIZE), (self.X, self.Y + self.SIZE)))
        elif index == 4:
            self.tileList.setTile(4,
                                  Tile(value, (self.SIZE, self.SIZE), (self.X + self.SIZE, self.Y + self.SIZE)))
        else:
            pass

    def networkThread(self) -> None:
        self.setTileColour(1, (1, 1, 1))

        inputs = [self.tileList.getTile(1).colourIndex,
                  self.tileList.getTile(2).colourIndex,
                  self.tileList.getTile(4).colourIndex,
                  self.tileList.getTile(3).colourIndex]

        for i in range(4):
            if inputs[i] >= 128:
                inputs[i] = 1
            else:
                inputs[i] = -1
            print(inputs[i])
        print("end")

        hl1 = [inputs[0] + inputs[3],
               inputs[1] + inputs[2],
               inputs[0] + inputs[3] * -1,
               inputs[1] + inputs[2] * -1]

        hl2 = [sigmoid(hl1[0] + hl1[1]),
               sigmoid(hl1[0] * -1 + hl1[1]),
               sigmoid(hl1[2] + hl1[3] * -1),
               sigmoid(hl1[2] + hl1[3])]

        print(hl2)

        solid = "false"
        vertical = "false"
        diagonal = "false"
        horizontal = "false"
        single = "false"

        if hl2[0] != 0.5:
            solid = "true"
        if hl2[1] != 0.5:
            vertical = "true"
        if hl2[2] != 0.5:
            diagonal = "true"
        if hl2[3] != 0.5:
            horizontal = "true"
        if hl2[0] != 0.5 and hl2[1] != 0.5 and hl2[2] != 0.5 and hl2[3] != 0.5 :
            solid = "false"
            vertical = "false"
            diagonal = "false"
            horizontal = "false"
            single = "true"

        self.setText("solid [" + solid + "], vertical [" + vertical + "], diagonal [" + diagonal + "], horizontal [" + horizontal
                     + "], single [" + single + "]")


if __name__ == "__main__":
    instance = Game()
    instance.loop()
