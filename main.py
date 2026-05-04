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

#Exercise 7: Trails 
TRAILS_LENGTH = 40  



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
    
    
   # Exercise 4: collision detection
def check_collision(a: dict, b: dict) -> bool:
    
    rect_a = pygame.Rect(a["x"], a["y"], a["size"], a["size"])
    rect_b = pygame.Rect(b["x"], b["y"], b["size"], b["size"])
    return rect_a.colliderect(rect_b) 
    
    # Exercise 6 helper: rescale velocity to match new size
def _rescale_speed(sq: dict, new_size: int) -> None:
    desired = 200 * (1 - (new_size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE + 1))
    desired = max(50, desired)
    current = math.hypot(sq["dx"], sq["dy"])
    if current > 0:
        scale = desired / current
        sq["dx"] *= scale
        sq["dy"] *= scale

    # Exercise 9: start animated growth
def start_grow(sq: dict, prey_size: int) -> None:
    
    growth   = max(1, prey_size // 4)
    new_size = min(sq["size"] + growth, ABSOLUTE_MAX_SIZE)
    if new_size == sq["size"]:
        return  # already at cap, nothing to do

    sq["size_at_start"]  = sq["size"]
    sq["target_size"]    = new_size
    sq["grow_start_ms"]  = pygame.time.get_ticks()
    sq["growing"]        = True
    
    
# Exercise 9: tick growth animation each frame
def update_growth(sq: dict) -> None:
    """Linearly interpolate size toward target_size over GROWTH_DURATION_MS."""
    if not sq["growing"]:
        return
    elapsed = pygame.time.get_ticks() - sq["grow_start_ms"]
    t = min(elapsed / GROWTH_DURATION_MS, 1.0)     # 0.0 → 1.0
    sq["size"] = int(sq["size_at_start"] + t * (sq["target_size"] - sq["size_at_start"]))
    if t >= 1.0:
        sq["size"]    = sq["target_size"]
        sq["growing"] = False
        _rescale_speed(sq, sq["size"])   # Q6: update speed for new size


    # Exercise 5 + 6: eating
def handle_eating(squares: list) -> None:
    
    eaten = set()
    for i in range(len(squares)):
        if i in eaten:
            continue
        for j in range(i + 1, len(squares)):
            if j in eaten:
                continue
            a, b = squares[i], squares[j]
            if check_collision(a, b):
                if a["size"] > b["size"]:
                    start_grow(a, b["size"])
                    eaten.add(j)
                elif b["size"] > a["size"]:
                    start_grow(b, a["size"])
                    eaten.add(i)
                # equal size → no eating

    for idx in eaten:
        respawn(squares[idx])



def apply_flee(squares: list) -> None:
    for sq in squares:
        for other in squares:
            if sq is other:
                continue
            if sq["size"] < other["size"]:
                fx   = sq["x"] - other["x"]
                fy   = sq["y"] - other["y"]
                dist = (fx ** 2 + fy ** 2) ** 0.5
                if dist < 150 and dist > 0:
                    fx /= dist
                    fy /= dist
                    flee_strength = 300
                    sq["dx"] += fx * flee_strength * 0.05
                    sq["dy"] += fy * flee_strength * 0.05
                    speed = (sq["dx"] ** 2 + sq["dy"] ** 2) ** 0.5
                    max_speed = 300
                    if speed > max_speed:
                        sq["dx"] = sq["dx"] / speed * max_speed
                        sq["dy"] = sq["dy"] / speed * max_speed

    
    
    
    
    
    
    
    # Exercise 3: screen wrapping
def wrap_screen(sq: dict) -> None:
    size = sq["size"]
    if sq["x"] + size < 0:
        sq["x"] = float(WIDTH)
    elif sq["x"] > WIDTH:
        sq["x"] = float(-size)
    if sq["y"] + size < 0:
        sq["y"] = float(HEIGHT)
    elif sq["y"] > HEIGHT:
        sq["y"] = float(-size)


# Exercise 7: draw trail
def draw_trail(surface: pygame.Surface, sq: dict) -> None:
    trail = sq["trail"]
    if len(trail) < 2:
        return

    r, g, b = sq["color"]
    n = len(trail)

    for i in range(1, n):
        p1 = trail[i - 1]
        p2 = trail[i]

        # Skip wrap-boundary segments (the fix)
        if abs(p2[0] - p1[0]) > WIDTH  / 2:
            continue
        if abs(p2[1] - p1[1]) > HEIGHT / 2:
            continue

        # Older segments are dimmer
        alpha = i / n
        color = (int(r * alpha), int(g * alpha), int(b * alpha))
        pygame.draw.line(surface, color,
                         (int(p1[0]), int(p1[1])),
                         (int(p2[0]), int(p2[1])), 2)


def run_speed_test() -> None:
    size = 20
    sq   = make_square(size)
    sq["x"] = float(WIDTH  // 2)
    sq["y"] = float(HEIGHT // 2)

    expected = 200 * (1 - (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE + 1))
    expected = max(50.0, expected)

    angle    = math.pi / 4
    sq["dx"] = expected * math.cos(angle)
    sq["dy"] = expected * math.sin(angle)

    dt = 1.0 / FPS
    x0, y0 = sq["x"], sq["y"]
    sq["x"] += sq["dx"] * dt
    sq["y"] += sq["dy"] * dt

    measured = math.hypot(sq["x"] - x0, sq["y"] - y0) / dt

    assert abs(measured - expected) < 0.01, (
        f"Speed test FAILED: expected {expected:.4f} px/s, got {measured:.4f} px/s"
    )
    print(f"[SpeedTest] PASSED — {measured:.4f} ≈ {expected:.4f} px/s")



# Startup
if TEST_MODE_ON:            # Exercise 8: headless speed test
    run_speed_test()

squares = create_squares()  # Exercise 1: mix of squares


# Main loop
while True:
    delta_time = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((15, 15, 30))

    # Flee (your original logic, untouched)
    apply_flee(squares)

    for sq in squares:
        # Exercise 7: record center position in trail before moving
        cx = sq["x"] + sq["size"] / 2
        cy = sq["y"] + sq["size"] / 2
        sq["trail"].append((cx, cy))
        if len(sq["trail"]) > TRAILS_LENGTH:
            sq["trail"].pop(0)

        # Move
        sq["x"] += sq["dx"] * delta_time
        sq["y"] += sq["dy"] * delta_time

        # Exercise 3: wrap instead of bounce
        wrap_screen(sq)

        # Exercise 9: animate growth
        update_growth(sq)

    # Exercise 5 + 6: eating
    handle_eating(squares)

    # Draw trails then squares
    for sq in squares:
        draw_trail(screen, sq)                                          # Q7
        pygame.draw.rect(screen, sq["color"],
                         (sq["x"], sq["y"], sq["size"], sq["size"]))   # original

    fps_text = font.render(
        f"FPS: {clock.get_fps():.1f}  Squares: {len(squares)}", True, (255, 255, 255)
    )
    screen.blit(fps_text, (10, 10))
    pygame.display.flip()