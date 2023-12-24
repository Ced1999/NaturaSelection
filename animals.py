from tile import *
import random
class Animal:
    def __init__(self, max_energy, x, y):
        self.max_energy = max_energy
        self.energy = max_energy
        self.x = x  # X-coordinate
        self.y = y  # Y-coordinate
        self.alive = True
    def random_move(self, world_width, world_height):
        """ Move the animal randomly within the bounds of the world """
        self.x = min(max(0, self.x + random.randint(-1, 1)), world_width - 1)
        self.y = min(max(0, self.y + random.randint(-1, 1)), world_height - 1)
        self.energy -= 10  # Decrease energy for moving
        self.check_energy()
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def move(self):
        self.energy -= 10
        self.check_energy()

    def eat(self, tile):
        raise NotImplementedError("This method should be overridden in subclasses")

    def check_energy(self):
        if self.energy <= 0:
            self.energy = 0
            self.alive = False
            self.on_death()

    def on_death(self):
        # Placeholder for any additional logic when the animal dies
        pass

    # Additional common methods for all animals can be added here
class Herbivore(Animal):
    def eat(self, tile):
        if tile.type == TileType.GRASS and tile.nutrients > 0:
            self.energy = min(self.energy + tile.nutrients, self.max_energy)
            tile.degrade()

    # Override or add additional methods specific to herbivores
class Carnivore(Animal):
    def eat(self, prey):
        if prey.alive :
            self.energy = min(self.energy + 20, self.max_energy)
            prey.alive = False
            prey.on_death()
    # Override or add additional methods specific to carnivores
