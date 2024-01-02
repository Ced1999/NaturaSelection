from tile import *
import random
from world import World

class Animal:
    def __init__(self, x, y, speed=2, sight=20):
        self.apples_collected = 0
        self.x = x  # X-coordinate
        self.y = y  # Y-coordinate
        self.alive = True
        self.speed = speed
        self.sight = sight
        self.energy = 500
        self.move_accumulator = 0.0

    def reset_energy(self):
        self.energy = 500
    def move(self, world):
        """ Move the animal with fractional speed accumulation """
        self.move_accumulator += self.speed % 1
        if self.move_accumulator >= 1.0:
            self.move_accumulator -= 1.0
            self.move_towards_food(world)

        for _ in range(int(self.speed)):
            self.move_towards_food(world)

        # Calculate and deduct energy cost
        self.energy -= ((self.speed) ** 2) + self.sight / 5
        if self.energy <= 0:
            self.alive = False
            self.on_death()

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
    def distance_to(self, x1, y1,x2,y2):
        """ Calculate the Manhattan distance from the animal to a given point """
        return abs(x1 - x2) + abs(y1-y2)
    def find_closest_apple(self,world):
        closest_x = None
        closest_y = None
        min_distance = float('inf')
        for y in range(max(0, self.y - self.sight), min(self.y + self.sight + 1, world.height)):
            for x in range(max(0, self.x - self.sight), min(self.x + self.sight + 1, world.width)):
                tile = world.get_tile(x,y)
                if tile.type == TileType.APPLE:
                    distance = self.distance_to(self.x,x,self.y,y)
                    if distance < min_distance:
                        min_distance = distance
                        closest_x = x
                        closest_y = y
        return closest_x,closest_y, min_distance
    def can_see_apple(self,world):
        for y in range(max(0, self.y - self.sight), min(self.y + self.sight + 1, world.height)):
            for x in range(max(0, self.x - self.sight), min(self.x + self.sight + 1, world.width)):
                if world.get_tile(x,y) == TileType.APPLE:
                    return True
        return False
    def move_towards_food(self, world):
        closest_apple_x, closest_apple_y, min_distance = self.find_closest_apple(world)

        if closest_apple_x is None or closest_apple_y is None:
            self.perform_random_move(world)
            return

        # Determine the direction for the next move
        move_x, move_y = 0, 0

        # Check if horizontal or vertical move is better
        if closest_apple_x != self.x:  # If not aligned with apple horizontally
            move_x = 1 if closest_apple_x > self.x else -1  # Move right if apple is to the right, else move left

        elif closest_apple_y != self.y:  # If not aligned with apple vertically
            move_y = 1 if closest_apple_y > self.y else -1  # Move down if apple is below, else move up

        # Calculate new position
        new_x = max(0, min(self.x + move_x, world.width - 1))
        new_y = max(0, min(self.y + move_y, world.height - 1))


        # Update position
        self.set_position(new_x, new_y)

    def perform_random_move(self, world):
        xpos = min(max(0, self.x + random.randint(-1, 1)), world.width - 1)
        ypos = min(max(0, self.y + random.randint(-1, 1)), world.height - 1)
        self.set_position(xpos, ypos)
    def reproduce(self):
        # Define mutation ranges
        speed_mutation_range = 0.1  # For example, speed can change by up to 10%
        sight_mutation_range = 1    # Sight can change by up to 1 unit

        # Calculate new attributes with mutation
        new_speed = self.speed + (random.random() * 2 - 1) * speed_mutation_range
        new_sight = max(1, self.sight + random.randint(-sight_mutation_range, sight_mutation_range))

        # Ensure new attributes are within sensible bounds
        new_speed = max(1, min(new_speed, 5))  # Assuming speed should be between 0.1 and 5
        new_sight = max(10, min(new_sight, 25))   # Assuming sight should be between 1 and 20

        # Create a new animal at the same location with mutated attributes
        new_animal = type(self)(self.x, self.y, new_speed, new_sight)
        return new_animal
        

class Herbivore(Animal):
    def eat(self, tile):
        if tile.type == TileType.APPLE:
            self.apples_collected += 1
            self.reset_energy()
            tile.type = TileType.GRASS
            return True
        return False
