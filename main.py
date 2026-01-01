import pygame
import sys
import random
import time
from pygame.math import Vector2
from text import *

# --- HK Rails ---
# tko
from HK import tko_line
from HK.tko_line import *




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

# --- Rails Colour
tko_line_colour = (100, 0, 100)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('W-T-F')
font = pygame.font.Font(None, 36)


station_circle_radius = 15


# --- TKO Line ---


# --- KT Line ---

kt_line_stations_branches = {
  
}

kt_line_stations_opened = {
  "TKL", "Yau Tong", 
  "Lam Tin", "KT", 
  "Ngau Tau Kok", "Kowloon Bay", 
  "Choi Hung", "Diamond Hill", 
  "Wong Tai Sin", "Lok Fu", 
  "Kowloon Tong", "Shek Kip Mei", 
  "Prince Edward", "Mong Kok", 
  "Yau Ma Tie", "Ho Man Tin", 
  "Whampoa"
}

# --- East Rail Line ---


# --- Camera Settings

zoom = 1.0
offset_x, offset_y = 0, 0
dragging = False
last_mouse_pos = (0, 0)

def transform(pos):
  # zooming and offset
  x, y = pos
  return int(x * zoom + offset_x), int(y * zoom + offset_y)

def main():
  global zoom, offset_x, offset_y, dragging, last_mouse_pos
  running = True
  while running:
    screen.fill(black)
    
    for station_name in (tko_line_stations_name):
      if tko_line_stations_opened[station_name]:
        for branch in (tko_line_stations_branches[station_name]):
          pygame.draw.line(screen, tko_line_colour, transform(tko_line_stations_pos[station_name]), transform(tko_line_stations_pos[branch]), 5)
          # pygame.draw.circle(screen, gray, tko_line_stations_pos[branch], station_circle_radius)
        pygame.draw.circle(screen, white, transform(tko_line_stations_pos[station_name]), int(station_circle_radius * zoom))
    
    mouse_pos = pygame.mouse.get_pos()
    
    zoom_in_button = pygame.Rect(10, 10, 50, 50)
    
    if zoom_in_button.collidepoint(mouse_pos):
      write(screen, zoom_in_button, "+", 65, "black", "gray69", 10)
    else:
      write(screen, zoom_in_button, "+", 65, "black", "white", 10)
    
    zoom_out_button = pygame.Rect(65, 10, 50, 50)
    
    if zoom_out_button.collidepoint(mouse_pos):
      write(screen, zoom_out_button, "-", 65, "black", "gray69", 10)
    else:
      write(screen, zoom_out_button, "-", 65, "black", "white", 10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        
          # --- Zooming (Keyboard) ---
          elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
            zoom *= 1.1
          elif event.key == pygame.K_MINUS:
            zoom /= 1.1
          
          # --- Screen Movements (Keyboard) ---
          elif event.key == pygame.K_LEFT:
            offset_x += 20
          elif event.key == pygame.K_RIGHT:
            offset_x -= 20
          elif event.key == pygame.K_UP:
            offset_y += 20
          elif event.key == pygame.K_DOWN:
            offset_y -= 20
        
        # --- Zooming (Mouse) ---
        
        # Mouse Wheel
        elif event.type == pygame.MOUSEWHEEL:
          if event.y > 0: # scroll up
            zoom *= 1.1
          elif event.y < 0: # scroll down
            zoom /= 1.1

        # --- Screen Movements (Mouse) ---
        
        # Mouse Drag
        # start
        elif event.type == pygame.MOUSEBUTTONDOWN:
          # Press button zooming
          if zoom_in_button.collidepoint(mouse_pos):
            zoom *= 1.1
          elif zoom_out_button.collidepoint(mouse_pos):
            zoom /= 1.1
          
          # Mouse move
          elif event.button == 1 and not(zoom_in_button.collidepoint(mouse_pos) or zoom_out_button.collidepoint(mouse_pos)): # left click
            dragging = True
            last_mouse_pos = event.pos
        
        # stop
        elif event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            dragging = False
        
        # Screen Move While Dragging
        elif event.type == pygame.MOUSEMOTION:
          if dragging:
            dx = event.pos[0] - last_mouse_pos[0]
            dy = event.pos[1] - last_mouse_pos[1]
            offset_x += dx
            offset_y += dy
            last_mouse_pos = event.pos          
  
    pygame.display.flip()
    clock.tick(fps)
  
main()
