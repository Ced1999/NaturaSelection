from enum import Enum

class TileType(Enum):
    GRASS = 1
    DIRT = 2
    WATER = 3

class Tile:
    def __init__(self, tile_type, nutrients=50, regrow_ticks=100):
        self.type = tile_type
        self.nutrients = nutrients
        self.regrow_ticks = regrow_ticks if tile_type == TileType.DIRT else 0

    def degrade(self):
        if self.type == TileType.GRASS:
            self.type = TileType.DIRT
            self.nutrients = 0
            self.regrow_ticks = 100  # Reset the tick counter for regrowth

    def regrow(self):
        if self.type == TileType.DIRT and self.regrow_ticks <= 0:
            self.type = TileType.GRASS
            self.nutrients = 100

    def decrement_regrow_tick(self):
        if self.type == TileType.DIRT and self.regrow_ticks > 0:
            self.regrow_ticks -= 1

    # Additional methods can be added here
