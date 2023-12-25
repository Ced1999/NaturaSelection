from tile import *
import random
class World:
    def __init__(self, width, height,apple_count):
        self.width = width
        self.height = height
        self.grid = [[Tile(TileType.GRASS) for _ in range(width)] for _ in range(height)]
        self.apple_count = apple_count
        self.place_apples(apple_count)
    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        else:
            raise IndexError(f"Tile coordinates ({x}, {y}) are out of bounds.")
    def place_apples(self,apple_count):
        for _ in range(apple_count):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if self.grid[x][y].type == TileType.GRASS:
                    self.grid[x][y] = Tile(TileType.APPLE)
                    break
    # Additional methods for world behavior can be added here
