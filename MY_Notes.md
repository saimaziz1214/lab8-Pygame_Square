# MY_NOTES.md - Lab 8 Part II


## Flee Feature - My thinking before coding

Before writing anything I tried to think through how fleeing would actually work.

So the idea is: a small square needs to know where the big square is, and move in the opposite direction. Simple enough in theory.



## Things I had to figure out

**Why normalize?**
At first I didn't get why you'd normalize the vector. Then I realized — if you don't, a square that's 10px away gets a huge force, and one that's 140px away gets almost nothing. Normalizing makes the force the same strength no matter the distance. Then you control the strength manually with flee_strength.

**Why clamp speed?**
Every frame we add a little flee force to dx and dy. If we never reset or limit it, the speed just keeps growing. After a few seconds the square would be flying across the screen at insane speed. Clamping puts a ceiling on it.

**The dist > 0 check**
I almost forgot this. If two squares are exactly on top of each other, dist = 0 and we'd be dividing by zero. Crash. So always check dist > 0 before dividing.



## Edge cases I thought about

- What if two squares are the same size? Neither flees from the other. The condition is strictly `sq["size"] < other["size"]` so equal sizes are ignored. Fine for now.
- What if a small square is surrounded by multiple big squares? It gets flee force from all of them added together. Could get chaotic but that's actually kind of cool behavior.
- What if a square is already at the wall and a big square is pushing it into the corner? It'll bounce off the wall. The wall bounce and flee force can fight each other a bit but it's not a big problem.



## FPS = 0 experiment

Tried it. The squares moved insanely fast and the CPU went to 100%. 

Why: with no FPS cap, the loop runs thousands of times per second. delta_time becomes super tiny but inconsistent frame to frame. Even with time-based movement, tiny floating point differences stack up and cause jittery behavior. Also pygame is doing thousands of draw calls per second which kills the CPU.


That would be cleaner. Right now all the logic is in the main loop which gets messy as we add features. Classes would help organize that. Maybe worth refactoring later.
