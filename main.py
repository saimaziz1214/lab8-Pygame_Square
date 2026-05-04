import pygame
import sys
import random
import math

pygame.init()

# ── Screen 
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

#Square size limits 
MIN_SIZE = 10
MAX_SIZE = 50

# Exercise 1: Mix of squares 
SQUARE_CONFIGS = [
    (5,  25),   # 5  squares of size 25 
    (10, 10),   # 10 squares of size 10 
    (30,  4),   # 30 squares of size  4 
]




def make_square(size: int) -> dict: 
   
    
    speed = 200 * (1 - (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE + 1))
    speed = max(50, speed)

    return {
        "x":             float(random.randint(0, max(0, WIDTH  - size))),
        "y":             float(random.randint(0, max(0, HEIGHT - size))),
        "dx":            random.choice([-1, 1]) * speed,
        "dy":            random.choice([-1, 1]) * speed,
        "size":          size,
        "original_size": size,          # Q2
        "color":         (random.randint(50, 255),
                          random.randint(50, 255),
                          random.randint(50, 255)),
        # Q7 – trail
        "trail":         [],
        # Q9 – animated growth
        "target_size":   size,
        "size_at_start": size,
        "grow_start_ms": 0,
        "growing":       False,
    }



# Exercise 1: create starting population
def create_squares() -> list:

    result = []
    for count, size in SQUARE_CONFIGS:
        for _ in range(count):
            result.append(make_square(size))
    return result

# Exercise 2: same-size respawn
def respawn(sq: dict) -> None:
    size  = sq["original_size"]
    speed = 200 * (1 - (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE + 1))
    speed = max(50, speed)

    sq["size"]          = size
    sq["target_size"]   = size
    sq["growing"]       = False
    sq["x"]             = float(random.randint(0, max(0, WIDTH  - size)))
    sq["y"]             = float(random.randint(0, max(0, HEIGHT - size)))
    sq["dx"]            = random.choice([-1, 1]) * speed
    sq["dy"]            = random.choice([-1, 1]) * speed
    sq["trail"]         = [] 