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

