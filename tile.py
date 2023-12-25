from enum import Enum

class TileType(Enum):
    GRASS = 1
    DIRT = 2
    WATER = 3
    APPLE = 4

class Tile:
    def __init__(self, tile_type):
        self.type = tile_type