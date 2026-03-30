import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")

# Global settings
NUM_SQUARES = 100
MIN_SIZE = 10
MAX_SIZE = 50
GLOBAL_MAX_SPEED = 5
JITTER = 0.3  # How much direction randomly changes per frame

clock = pygame.time.Clock()

def make_square():
    size = random.randint(MIN_SIZE, MAX_SIZE)
    # Bigger = slower: max_speed is inversely proportional to size
    max_speed = GLOBAL_MAX_SPEED * (1 - (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE + 1))
    max_speed = max(0.5, max_speed)  # Ensure minimum movement
    speed = random.uniform(0.5, max_speed)
    return {
        "x": random.randint(0, WIDTH - size),
        "y": random.randint(0, HEIGHT - size),
        "size": size,
        "dx": random.choice([-1, 1]) * speed,
        "dy": random.choice([-1, 1]) * speed,
        "max_speed": max_speed,
        "color": (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255)),
    }

# Create 100 squares
squares = [make_square() for _ in range(NUM_SQUARES)]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((15, 15, 30))  # Dark background

    for sq in squares:
        # Jitter: randomly nudge direction a little
        sq["dx"] += random.uniform(-JITTER, JITTER)
        sq["dy"] += random.uniform(-JITTER, JITTER)

        # Clamp speed to this square's max_speed
        speed = (sq["dx"] ** 2 + sq["dy"] ** 2) ** 0.5
        if speed > sq["max_speed"]:
            scale = sq["max_speed"] / speed
            sq["dx"] *= scale
            sq["dy"] *= scale

        # Move
        sq["x"] += sq["dx"]
        sq["y"] += sq["dy"]

        # Bounce off walls
        if sq["x"] <= 0 or sq["x"] + sq["size"] >= WIDTH:
            sq["dx"] *= -1
            sq["x"] = max(0, min(WIDTH - sq["size"], sq["x"]))
        if sq["y"] <= 0 or sq["y"] + sq["size"] >= HEIGHT:
            sq["dy"] *= -1
            sq["y"] = max(0, min(HEIGHT - sq["size"], sq["y"]))

        pygame.draw.rect(screen, sq["color"], (sq["x"], sq["y"], sq["size"], sq["size"]))

    pygame.display.flip()
    clock.tick(60)