import sys
from world import World
from animals import Animal,Herbivore,Carnivore
import pygame
from tile import *
import random

# Constants for rendering
TILE_SIZE = 10
HERBIVORE_COLOR = (0, 255, 0)  # Green
CARNIVORE_COLOR = (255, 0, 0)  # Red
GRASS_COLOR = (0, 128, 0)      # Dark Green
DIRT_COLOR = (101, 67, 33)     # Brown
WATER_COLOR = (0, 0, 255)      # Blue

def render(screen, world, animals):
    for y in range(world.height):
        for x in range(world.width):
            tile = world.get_tile(x, y)
            if tile.type == TileType.GRASS:
                color = GRASS_COLOR
            elif tile.type == TileType.DIRT:
                color = DIRT_COLOR
            elif tile.type == TileType.WATER:
                color = WATER_COLOR

            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for animal in animals:
        if animal.alive:
            # Determine the color based on the type of animal
            color = HERBIVORE_COLOR if isinstance(animal, Herbivore) else CARNIVORE_COLOR
            
            # Calculate the position for drawing the animal
            animal_x = animal.x * TILE_SIZE + TILE_SIZE // 2
            animal_y = animal.y * TILE_SIZE + TILE_SIZE // 2

            # Draw the animal
            pygame.draw.circle(screen, color, (animal_x, animal_y), TILE_SIZE // 2)

            # Draw the energy bar above the animal
            energy_ratio = animal.energy / animal.max_energy
            energy_bar_length = TILE_SIZE * energy_ratio
            energy_bar_color = (255 - int(255 * energy_ratio), int(255 * energy_ratio), 0)  # From red to green
            pygame.draw.rect(screen, energy_bar_color, (animal_x - TILE_SIZE // 2, animal_y - TILE_SIZE // 2 - 5, energy_bar_length, 2))

    pygame.display.flip()


def run_simulation():
    # Initialize Pygame
    pygame.init()

    # Set up the Pygame screen


    # Initialize the world and animals
    world = World(50, 50)  # Example world size
    animals = [Herbivore(100, random.randint(0,world.height), random.randint(0,world.width)) for _ in range(30)]
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
                animal.eat(current_tile)
        world.update()

        # Render the world and animals
        render(screen, world, animals)

        pygame.time.delay(200)

    pygame.quit()
