from simulation import *
print("Do you want to run the simulation with default values= Y/N ?")
default = input()
if default in ("Y","y"):
    run_simulation()
else:
    print(f"Enter the starting value for animal speed: (range 1-5)")
    speed = int(input())
    print("Enter the starting value for animal sight: (Range 10-25)")
    sight = int(input())
    print("Enter the starting amount of animals: ")
    animal_count = int(input())
    print("Enter the starting amount of apples: ")
    apple_count = int(input())
    run_simulation(speed,sight,animal_count,apple_count,)