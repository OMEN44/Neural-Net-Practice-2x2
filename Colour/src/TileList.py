from Colour.src.Tile import Tile


class TileList:
    def __init__(self):
        self.colour1 = None
        self.colour2 = None
        self.colour3 = None
        self.colour4 = None

    def setTile(self, num, tile: Tile):
        if num == 1:
            self.colour1 = tile
        elif num == 2:
            self.colour2 = tile
        elif num == 3:
            self.colour3 = tile
        elif num == 4:
            self.colour4 = tile

    def getTile(self, num) -> Tile:
        if num == 1:
            return self.colour1
        elif num == 2:
            return self.colour2
        elif num == 3:
            return self.colour3
        elif num == 4:
            return self.colour4

    def getList(self) -> list:
        return [self.colour1, self.colour2, self.colour3, self.colour4]
