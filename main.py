import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Squares")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

MIN_SIZE = 10
MAX_SIZE = 50
NUM_SQUARES = 20

def make_square():
    size = random.randint(MIN_SIZE, MAX_SIZE)
    speed = 200 * (1 - (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE + 1))
    speed = max(50, speed)
    return {
        "x": float(random.randint(0, WIDTH - size)),
        "y": float(random.randint(0, HEIGHT - size)),
        "dx": random.choice([-1, 1]) * speed,
        "dy": random.choice([-1, 1]) * speed,
        "size": size,
        "color": (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
    }

def apply_flee(squares):
    for sq in squares:
        for other in squares:
            if sq is other:
                continue
            if sq["size"] < other["size"]:
                fx = sq["x"] - other["x"]
                fy = sq["y"] - other["y"]
                dist = (fx**2 + fy**2) ** 0.5
                if dist < 150 and dist > 0:
                    fx /= dist
                    fy /= dist
                    flee_strength = 300
                    sq["dx"] += fx * flee_strength * 0.05
                    sq["dy"] += fy * flee_strength * 0.05
                    speed = (sq["dx"]**2 + sq["dy"]**2) ** 0.5
                    max_speed = 300
                    if speed > max_speed:
                        sq["dx"] = sq["dx"] / speed * max_speed
                        sq["dy"] = sq["dy"] / speed * max_speed

squares = [make_square() for _ in range(NUM_SQUARES)]

while True:
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((15, 15, 30))

    apply_flee(squares)

    for sq in squares:
        sq["x"] += sq["dx"] * delta_time
        sq["y"] += sq["dy"] * delta_time

        if sq["x"] <= 0 or sq["x"] + sq["size"] >= WIDTH:
            sq["dx"] *= -1
            sq["x"] = max(0.0, min(float(WIDTH - sq["size"]), sq["x"]))
        if sq["y"] <= 0 or sq["y"] + sq["size"] >= HEIGHT:
            sq["dy"] *= -1
            sq["y"] = max(0.0, min(float(HEIGHT - sq["size"]), sq["y"]))

        pygame.draw.rect(screen, sq["color"], (sq["x"], sq["y"], sq["size"], sq["size"]))

    fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()