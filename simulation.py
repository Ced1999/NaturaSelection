import sys
from world import World
from animals import Animal,Herbivore
import pygame
from tile import *
import random

# Constants for rendering
TILE_SIZE = 10
HERBIVORE_COLOR = (0, 255, 0)  # Green
APPLE_COLOR = (255, 0, 0)  # Red
GRASS_COLOR = (0, 128, 0)      # Dark Green
DIRT_COLOR = (101, 67, 33)     # Brown
WATER_COLOR = (0, 0, 255)      # Blue

def render(screen, world, animals):
    for y in range(world.height):
        for x in range(world.width):
            tile = world.get_tile(x, y)

            # Draw the base tile (grass, dirt, or water)
            if tile.type == TileType.GRASS:
                base_color = GRASS_COLOR
            elif tile.type == TileType.DIRT:
                base_color = DIRT_COLOR
            elif tile.type == TileType.WATER:
                base_color = WATER_COLOR
            else:
                base_color = GRASS_COLOR  # Default to grass for other types
            pygame.draw.rect(screen, base_color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            # If the tile has an apple, draw a red circle on top
            if tile.type == TileType.APPLE:
                apple_x = x * TILE_SIZE + TILE_SIZE // 2
                apple_y = y * TILE_SIZE + TILE_SIZE // 2
                pygame.draw.circle(screen, APPLE_COLOR, (apple_x, apple_y), TILE_SIZE // 2)
    for animal in animals:
        if animal.alive:
            # Determine the color based on the type of animal
            color = HERBIVORE_COLOR 
            # Calculate the position for drawing the animal
            animal_x = animal.x * TILE_SIZE + TILE_SIZE // 2
            animal_y = animal.y * TILE_SIZE + TILE_SIZE // 2

            # Draw the animal
            pygame.draw.circle(screen, color, (animal_x, animal_y), TILE_SIZE // 2)


    pygame.display.flip()


def run_simulation():
    # Initialize Pygame
    pygame.init()

    # Set up the Pygame screen


    # Initialize the world and animals
    world = World(50, 50,20)  # Example world size
    animals = [Herbivore(random.randint(0,world.height), random.randint(0,world.width)) for _ in range(60)]
    screen = pygame.display.set_mode((world.width * TILE_SIZE, world.height * TILE_SIZE))
    pygame.display.set_caption("Ecosystem Simulation")
    # Main simulation loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for animal in animals:
            if animal.alive:
                animal.move(world)
                current_tile = world.get_tile(animal.x, animal.y)
                if animal.eat(current_tile):
                    world.apple_count -= 1
        if not world.apple_count:
            #The Day is over
            for animal in animals:
                if animal.apples_collected == 0:
                    animal.alive = False
                    animal.on_death()
            world.apple_count = 20
            world.place_apples(20)

        # Render the world and animals
        render(screen, world, animals)

        pygame.time.delay(20)

    pygame.quit()
