import sys
from world import World
from animals import Animal,Herbivore
import pygame
from tile import *
import random
import statistics

# Constants for rendering
TILE_SIZE = 10
HERBIVORE_COLOR = (0, 255, 0)  # Green
APPLE_COLOR = (255, 0, 0)  # Red
GRASS_COLOR = (0, 128, 0)      # Dark Green
DIRT_COLOR = (101, 67, 33)     # Brown
WATER_COLOR = (0, 0, 255)      # Blue
TICKS_PER_DAY = 60
def render(screen, world, animals,show_sight_range):
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
            if show_sight_range:
                # Draw the sight range
                pygame.draw.circle(screen, (0, 0, 255, 50), (animal_x, animal_y), animal.sight * TILE_SIZE, 1)

    pygame.display.flip()


def run_simulation(speed=2,sight=15,animal_count=50,apple_count=30):
    # Initialize Pygame
    pygame.init()
    show_sight_range = False
    # Set up the Pygame screen
    world = World(50, 50, apple_count)  # Example world size
    animals = [Herbivore(random.randint(0, world.height - 1), random.randint(0, world.width - 1),speed,sight) for _ in range(animal_count)]
    screen = pygame.display.set_mode((world.width * TILE_SIZE, world.height * TILE_SIZE))
    pygame.display.set_caption("Ecosystem Simulation")

    # Main simulation loop
    running = True
    tick_counter = 0  # Initialize tick counter

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    show_sight_range = not show_sight_range

        for animal in animals:
            if animal.alive:
                animal.move(world)
                current_tile = world.get_tile(animal.x, animal.y)
                if animal.eat(current_tile):
                    world.apple_count -= 1

        # Increase tick counter
        tick_counter += 1

        # Check if a new day should start
        if not world.apple_count or tick_counter >= TICKS_PER_DAY:
            tick_counter = 0  # Reset tick counter for the new day
            new_animals = []
            for animal in animals:
                if animal.apples_collected == 0:
                    animal.alive = False
                    animal.on_death()
                if animal.apples_collected == 1:
                    animal.apples_collected = 0
                if animal.apples_collected >= 2 and animal.alive:
                    animal.apples_collected = 0
                    animal.reset_energy()
                    new_animal = animal.reproduce()
                    new_animals.append(new_animal)
            animals.extend(new_animals)
            world.apple_count = apple_count
            world.clear_and_place_apples(apple_count)
            speeds = [animal.speed for animal in animals if animal.alive]
            sights = [animal.sight for animal in animals if animal.alive]
            if speeds and sights:
                median_speed = statistics.mean(speeds)
                median_sight = statistics.mean(sights)
                
                print(f"median speed: {median_speed}, median sight: {median_sight}, number of animals {len(speeds)}")
        # Render the world and animals
        render(screen, world, animals,show_sight_range)

        pygame.time.delay(1)

    pygame.quit()

