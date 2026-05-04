# MY_EXAM.md

## Exercise 7

### what is the visual artifact

so basically when a square wraps around the screen (like it goes off the right side and comes back on the left), the trail doesnt know that happened. it still has the last position stored which was near the right edge (x close to WIDTH) and the next position is suddenly near x=0 on the left side.

so when pygame draws a line between those two points it just draws a straight line all the way across the screen. looks like a big glitch slash diagonal line cutting through everything, really obvious visually.

### how i fixed it

before drawing each segment of the trail i check if the two points are too far apart. if the difference in x is more than half the screen width, or the difference in y is more than half the screen height, that means a wrap happened so i just skip drawing that segment.

```python
dx = abs(p2[0] - p1[0])
dy = abs(p2[1] - p1[1])
if dx > WIDTH / 2 or dy > HEIGHT / 2:
    continue  # wrap happened, skip this line
```

also when a square respawns i clear the trail list completly so there are no leftover positions from its previous life that could cause more artifacts.



## Exercise 8

### speed test analysis

the goal here is to make sure a square is actually moving at the speed we expect it to.

my assumption is that speed = 200 * (1 - (size - MIN_SIZE) / (MAX_SIZE - MIN_SIZE + 1)) with a minimum of 50. so if i know the size i can calculate what the speed should be.

what i actually test:
1. make a square with a known size (i used size 20)
2. put it right in the middle of the screen so it wont wrap during the test
3. manually set vx and vy to the expected speed at a 45 degree angle so i know exactly what direction its going
4. save the starting x and y
5. do one movement step with dt = 1/60
6. measure how far it moved using math.hypot
7. divide by dt to get the measured speed
8. assert that measured speed and expected speed are within 0.01 of each other

i used a global flag TEST_MODE_ON so the test only runs if you set it to True, otherwise the normal simulation just runs normally. the test doesnt need a pygame window at all which is nice.


## Exercise 15

### S.A.C test analysis

S.A.C = Separation Alignment Cohesion. the idea is to check that the boids are actually flocking properly and not just moving randomly.

the way i thought about it is - if flocking is working you should be able to measure 3 things:

**alignment** - all the boids should start pointing in roughly the same direction after a while. i measure this using circular variance of the velocity angles. i get each boids angle with math.atan2(vy, vx) then compute 1 - |mean unit vector|. if this value goes down compared to the start then alignment is working because at the start all angles are random so variance is high, after running for a bit they should align so variance drops.

**separation** - boids shouldnt be stacking on top of eachother. i measure the average nearest neighbour distance (for each boid find its closest neighbour, then average all those distances). if separation is working this should stay above some minimum threshold like BOID_SIZE * 2. if boids were just piling up this number would be close to 0.

**cohesion** - boids should group together not spread out randomly. i measure the standard deviation of all the x positions and y positions. at the start when everything is random the std is high. after the simulation runs for a while with cohesion on the boids should cluster so std should go down.

to run the test i simulate headlessly for about 300 frames (no window), measure before and after, then assert all three conditions. i toggle all behaviors ON at the start of the test so all three rules are active.

---

## Exercise 16

the implementation is in run_sac_test() in boids_exam.py.

the three asserts i do are:
1. var_after < var_before — checks alignment got better
2. sep_after > BOID_SIZE * 2 — checks boids kept personal space
3. std_after < std_before * 0.95 — checks boids grouped together (at least 5% reduction)

to run it just uncomment the run_sac_test() line at the bottom of boids_exam.py. it prints PASS or FAIL for each one with the actual numbers so its easy to debug if something is off.
