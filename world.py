from tile import *
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Tile(TileType.GRASS) for _ in range(width)] for _ in range(height)]

    def update(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                tile.decrement_regrow_tick()  # Decrement the tick counter
                if tile.type == TileType.DIRT:
                    tile.regrow()  # Attempt to regrow if the counter reaches 0

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            raise IndexError(f"Tile coordinates ({x}, {y}) are out of bounds.")

    # Additional methods for world behavior can be added here
