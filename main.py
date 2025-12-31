import pygame
import sys
import random
import time
from pygame.math import Vector2
from HK import *

pygame.init()

display_info = pygame.display.Info()
# width, height = display_info.current_w, display_info.current_h
width, height = 800, 600
fps = 60
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (200, 200, 200)
orange = (255, 165, 0)
light_blue = (173, 116, 233)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('W-T-F')
font = pygame.font.Font(None, 36)


station_circle_radius = 15


# --- TKO line ---

tko_line_stations_pos = {
  "Po Lam": (100, 100), 
  "Hang Hau": (100, 150), 
  "TKO": (150, 150), 
  "TKL": (200, 150), 
  "KT": (250, 150), 
  "Qurry Bay": (250, 300), 
  "North Point": (300, 300)
}

tko_line_stations_branched = {
  "Po Lam": ["Hang Hau"], 
  "Hang Hau": ["Po Lam"], 
  "TKO": ["Hang Hau", "LOHAS Park", "TKL"], 
  "TKL": ["TKO", "KT"], 
  "KT": ["TKL", "Qurry Bay"], 
  "Qurry Bay": ["KT", "North Point"], 
  "North Point": ["Qurry Bay"]
}

tko_line_stations_opened = {
  "Po Lam": True, 
  "Hang Hau": False, 
  "TKO": False, 
  "TKL": False, 
  "KT": False,
  "Qurry Bay": False, 
  "North Point": False
}


# --- KT line ---


# --- East Rail line ---



def main():
  running = True
  while running:
    screen.fill(black)
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
  
    pygame.display.flip()
  
main()