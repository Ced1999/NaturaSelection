from tile import *
import random
from world import World
class Animal:
    def __init__(self, x, y):
        self.apples_collected = 0
        self.x = x  # X-coordinate
        self.y = y  # Y-coordinate
        self.alive = True
    def move(self, world):
        """ Move the animal randomly within the bounds of the world """
        xpos = min(max(0, self.x + random.randint(-1, 1)), world.width - 1)
        ypos = min(max(0, self.y + random.randint(-1, 1)), world.height - 1)
        self.set_position(xpos,ypos)
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def eat(self, tile):
        raise NotImplementedError("This method should be overridden in subclasses")

    def on_death(self):
        # Placeholder for any additional logic when the animal dies
        pass

    # Additional common methods for all animals can be added here
class Herbivore(Animal):
    def eat(self, tile):
        if tile.type == TileType.APPLE:
            self.apples_collected+=1
            tile.type = TileType.GRASS
            return True
        return False

    # Override or add additional methods specific to herbivores
