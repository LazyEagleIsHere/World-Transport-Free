import pygame
import sys
import random
import time
from pygame.math import Vector2

pygame.init()

def hk_mtr():
  
  purple = (100, 0, 100)
  
  route = {
    "TKO line": [
      "Po Lam", "Hang Hau", "TKO", "TKL", "KT", "Qurry Bay", "North Point"
    ]
  }
  
  
  
  pygame.display.flip()