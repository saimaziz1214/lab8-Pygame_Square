# Lab 8 - Part II: Moving Squares
**Course:** Generative AI for Software Engineering - EPITA 2026
**Student:** Muhammad Saim Chaudhary
**Date:** April 2026

---

## What this lab was about

So this week we continued working on the moving squares project from last week. The main thing we had to do was add a flee behavior basically make the smaller squares run away from the bigger ones when they get too close. We also had to fix the way movement worked, switching from framebased to time based animation.

---

## The animation issue

Honestly I didn't fully understand why it mattered at first. But when I tried setting FPS to 0 and ran the app, the squares went crazy and my CPU spiked to 100%. That's when it clicked.

The problem with frame-based movement is that the speed depends on how fast your machine is. So:

python
x += dx  # old way - tied to frame rate

isn't reliable. The fix is to multiply by delta_time:


x += dx * delta_time  # new way consistent on any machine


delta_time is just how many seconds passed since the last frame. You get it from:


delta_time = clock.tick(FPS) / 1000.0


Simple change but it makes a big difference.



## The flee feature

This was the main challenge of the lab. The idea is: if a small square gets within 150 pixels of a bigger one, it should start moving away from it.

I had to think about it before writing anything. The way I approached it:

- find the direction from the big square to the small one (just subtract their positions)
- normalize it so the speed is consistent regardless of distance
- add that direction to the small square's velocity
- clamp the speed so it doesn't keep accelerating forever

The normalization part confused me at first. But basically if you don't normalize, a square that's very close will flee way faster than one that's a bit further. Normalizing makes the force always the same strength.


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
                    sq["dx"] += fx * 300 * 0.05
                    sq["dy"] += fy * 300 * 0.05
                    speed = (sq["dx"]**2 + sq["dy"]**2) ** 0.5
                    if speed > 300:
                        sq["dx"] = sq["dx"] / speed * 300
                        sq["dy"] = sq["dy"] / speed * 300


I also made a mistake early on where I defined the function but forgot to actually call it in the main loop. Spent a few minutes wondering why nothing was happening.



## FPS counter

We added a small HUD showing the current FPS. Nothing fancy:


fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
screen.blit(fps_text, (10, 10))


Useful for debugging, especially when testing the FPS=0 thing.


## Dicts vs Classes

We used dicts for the squares. Something like:


{"x": 100.0, "y": 200.0, "dx": 3.0, "size": 30, "color": (255, 0, 0)}


It works fine for this project. Classes would make more sense if the project got bigger, because you could give each square its own methods like `update()` or `draw()` instead of handling everything in the main loop. For now dicts are easier to read and get the job done.



## How I used CoPilot

I tried to use it only when I was stuck on understanding something, not to write code for me. The prompts I used were things like:

- "explain what delta_time is and why we need it, don't give me code"
- "why do we normalize a vector in flee behavior, simple explanation"
- "why does FPS=0 cause instability, explain simply"

That approach actually helped more than just asking for code, because I understood what I was writing instead of just pasting something in.


## Issues I ran into

The biggest headache was the Python environment. I kept running the script with `/opt/homebrew/bin/python3` which ignored the virtual environment completely, so pygame wasn't found. The fix was simple — just use `python3 main.py` while the venv is active — but it took a while to figure out what was going wrong.

Other than that, forgetting to call `apply_flee()` in the loop, and getting confused about vector normalization for a bit.



## What I took away from this

Time-based animation is just the right way to do it. The flee behavior was more math than I expected but once I drew it out on paper it made sense. And using CoPilot to explain rather than code actually made me learn more than I usually do.