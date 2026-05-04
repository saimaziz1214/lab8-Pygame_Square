

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