import pygame
import sys
import random
import time
from pygame.math import Vector2
from text import *

# --- HK Rails ---
from HK import *

# all
from HK.branched_line import *

# --- Trains ---
from trains import *



pygame.init()

display_info = pygame.display.Info()
width, height = display_info.current_w, display_info.current_h
# width, height = 800, 600
fps = 60
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (200, 200, 200)
orange = (255, 165, 0)
light_blue = (173, 116, 233)
blue = (0, 0, 200)
green = (0, 100, 0)

# --- Rails Colour
tko_line_colour = (100, 0, 100)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('W-T-F')
font = pygame.font.Font(None, 36)


station_circle_radius = 10

# --- Camera Settings

zoom = 1.0
# offset_x, offset_y = -(width // 100000), -(height // 100)
offset_x, offset_y = 450, 0
dragging = False
last_mouse_pos = (0, 0)

def transform(pos):
  # zooming and offset
  x, y = pos
  return int(x * zoom + offset_x), int(y * zoom + offset_y)


def draw(name, pos, r, labels_drawn):
  size = max(12, min(int(36 * zoom), 72))
  font = pygame.font.Font(None, size)
  text_surface = font.render(name, True, white)
  text_rect = text_surface.get_rect()
  
  offsets = [i for i in range(100)]
  dir = [
    lambda i: (pos[0] + r + i, pos[1] - text_rect.height // 2), # right
    lambda i: (pos[0] - r - text_rect.width - i, pos[1] - text_rect.height // 2), # left
    lambda i: (pos[0] - text_rect.width // 2, pos[1] - r - text_rect.height - i), # up
    lambda i: (pos[0] - text_rect.width // 2, pos[1] + r + i), # bottom
    lambda i: (pos[0] + r + i, pos[1] - r - i), # top right
    lambda i: (pos[0] - r - text_rect.width - i, pos[1] - r - i), # top left
    lambda i: (pos[0] + r + i, pos[1] + r + i), # bottom right
    lambda i: (pos[0] - r - text_rect.width - i, pos[1] + r + i) # bottom left
  ]
  
  for off in offsets:
    for d in dir:
      cx, cy = d(off)
      text_rect.topleft = (cx, cy)
      if not any(text_rect.colliderect(i) for i in labels_drawn):
        screen.blit(text_surface, text_rect)
        labels_drawn.append(text_rect)
        return
  
  # place below
  text_rect.topleft = (pos[0] - text_rect.width // 2, pos[1] + r + 120)
  screen.blit(text_surface, text_rect)
  labels_drawn.append(text_rect)


def train_page():
  running = True
  while running:
    screen.fill(black)

    mouse_pos = pygame.mouse.get_pos()
    
    home_button_size = (100, 100)
    home_button_pos = (width - home_button_size[0], height - home_button_size[1])
    home_button = pygame.Rect(home_button_pos, home_button_size)
    write(screen, home_button, 'X', 65, "black", "gray69" if home_button.collidepoint(mouse_pos) else "white", 10)
    
    trains_block_spacing = 10
    train_button_size = (width, 100)
    trains_cnt = 0
    for name in trains:
      train_button_pos = (0, train_button_size[1] * trains_cnt)
      trains_cnt += 1
      trains_button = pygame.Rect(train_button_pos, train_button_size)
      write(screen, trains_button, f"{name}    Fuel: {trains[name]["fuel"]}", 65, "black", "gray69" if trains_button.collidepoint(mouse_pos) else "white", 10)
      # pygame.draw.rect(screen, gray, (int(bottom_block_pos[0]), int(bottom_block_pos[1]), bottom_block_size[0], bottom_block_size[1]))
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False
          pygame.quit()
          sys.exit()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if home_button.collidepoint(mouse_pos):
          running = False
    
    pygame.display.flip()

def main():
  global zoom, offset_x, offset_y, dragging, last_mouse_pos, money, trains
  money = 3000
  trains = {
    "Steamer": {"pos": "", "engines": 1, "fuel car": 0, "run": False, "fuel": 1000}, 
  }
  running = True
  last_station_pressed = []
  while running:
    screen.fill(green)

    # for station_name in (tko_line_stations_name):
    #   if tko_line_stations_opened[station_name]:
    #     for branch in (tko_line_stations_branches[station_name]):
    #       pygame.draw.line(screen, tko_line_colour, transform(tko_line_stations_pos[station_name]), transform(tko_line_stations_pos[branch]), 5)
    #       # pygame.draw.circle(screen, gray, tko_line_stations_pos[branch], station_circle_radius)
    #     pygame.draw.circle(screen, white, transform(tko_line_stations_pos[station_name]), int(station_circle_radius * zoom))
    
    mouse_pos = pygame.mouse.get_pos()
    
    button_spacing = 55
    button_size = (50, 50)
    
    
    zoom_in_button_pos = (10, 10)
    zoom_in_button = pygame.Rect(zoom_in_button_pos, button_size)
    write(screen, zoom_in_button, '+', 65, "black", "gray69" if zoom_in_button.collidepoint(mouse_pos) else "white", 10)
    
    zoom_out_button_pos = (zoom_in_button_pos[0] + button_spacing, zoom_in_button_pos[1])
    zoom_out_button = pygame.Rect(zoom_out_button_pos, button_size)
    write(screen, zoom_out_button, '-', 65, "black", "gray69" if zoom_out_button.collidepoint(mouse_pos) else "white", 10)
    
    reverse_button_pos = (zoom_out_button_pos[0] + button_spacing, zoom_in_button_pos[1])
    reverse_button = pygame.Rect(reverse_button_pos, button_size)
    write(screen, reverse_button, '<--', 65, "black", "gray69" if reverse_button.collidepoint(mouse_pos) else "white", 10)
    
    rezoom_button_pos = (reverse_button_pos[0] + button_spacing, zoom_in_button_pos[1])
    rezoom_button = pygame.Rect(rezoom_button_pos, button_size)
    write(screen, rezoom_button, 'e', 65, "black", "gray69" if rezoom_button.collidepoint(mouse_pos) else "white", 10)
    
    ordered_stations = sorted(station_name, key = lambda n: (stations_pos[n][0], stations_pos[n][1]))
    
    labels_drawn = []
    drawn_stations = set()
    
    for name in ordered_stations:
      if station_opened[name]:
        pos = transform(stations_pos[name])
        for branch in stations_branches[name]:
          pos_branch = transform(stations_pos[branch])
          colour = white if station_opened[branch] else gray
          pygame.draw.line(screen, colour, pos, pos_branch, 5)
    
    # for name in ordered_stations:
    #   if station_opened[name] or not(name in drawn_stations):
    #     pos = transform(stations_pos[name])
    #     r = int(station_circle_radius * zoom)
    #     pygame.draw.circle(screen, white, pos, r)
    #     draw(name, pos, r, labels_drawn)
    #     drawn_stations.add(name)
    
    for name in ordered_stations:
      if station_opened[name] and name not in drawn_stations:
        pos = transform(stations_pos[name])
        r = int(station_circle_radius * zoom)
        pygame.draw.circle(screen, white, pos, r)
        # draw(name, pos, r, labels_drawn)
        # drawn_stations.add(name)
    
    for name in ordered_stations:
      if station_opened[name]:
        for branch in stations_branches[name]:
          if not(branch in drawn_stations):
            pos_branch = transform(stations_pos[branch])
            r_branch = int(station_circle_radius * zoom)
            colour = white if station_opened[branch] else gray
            pygame.draw.circle(screen, colour, pos_branch, r_branch)
            # draw(branch, pos_branch, r_branch, labels_drawn)
            # drawn_stations.add(branch)
    
    # for name in (station_name):
    #   if station_opened[name]:
    #     pos = transform(stations_pos[name])
    #     r = int(station_circle_radius * zoom)
    #     for branch in (stations_branches[name]):
    #       # print("E")
    #       pos_branch = transform(stations_pos[branch])
    #       r_branch = int(station_circle_radius * zoom)
    #       if station_opened[branch]:
    #         pygame.draw.line(screen, white, pos, pos_branch, 5)
    #         pygame.draw.circle(screen, white, pos_branch, r_branch)
    #       else:
    #         pygame.draw.line(screen, gray, pos, pos_branch, 5)
    #         pygame.draw.circle(screen, gray, pos_branch, r_branch)

    #       draw(branch, pos_branch, r_branch, labels_drawn)
    #     pygame.draw.circle(screen, white, pos, r)
        
    #     # station name
    #     draw(name, pos, r, labels_drawn)

    
    # --- Outlook ---
    
    # money += 5000
    
    bottom_block_size = (width, 100)
    bottom_block_pos = (0, height - bottom_block_size[1])
    pygame.draw.rect(screen, gray, (int(bottom_block_pos[0]), int(bottom_block_pos[1]), bottom_block_size[0], bottom_block_size[1]))
    
    info_y = bottom_block_pos[1] + 50
    info_spacing = 75
    
    money_text = font.render(f"${money}", True, black)
    money_rect = money_text.get_rect(topleft = (10 + info_spacing, info_y))
    pygame.draw.rect(screen, white, money_rect.inflate(10, 10))
    screen.blit(money_text, money_rect)
    
    menu_button = pygame.Rect(width - 250, bottom_block_pos[1] + 25, len("Settings") * 25, 50)
    write(screen, menu_button, "Menu", 65, "black", "gray69" if menu_button.collidepoint(mouse_pos) else "yellow", 10)
    
    all_trains_button = pygame.Rect(width - 100, 10, 50, 50)
    cnt = 0
    for name in trains:
      if not trains[name]["run"]:
        cnt += 1
    write(screen, all_trains_button, str(cnt), 65, "black", "gray69" if all_trains_button.collidepoint(mouse_pos) else "yellow", 10)
    
    
    buttons_movements = 50
    
    zoom_range = (2, 0.7)
    
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
            zoom = min(zoom_range[0], zoom * 1.1)
          elif event.key == pygame.K_MINUS:
            zoom = max(zoom_range[1], zoom / 1.1)
          
          # --- Screen Movements (Keyboard) ---
          elif event.key == pygame.K_LEFT:
            offset_x += buttons_movements
          elif event.key == pygame.K_RIGHT:
            offset_x -= buttons_movements
          elif event.key == pygame.K_UP:
            offset_y += buttons_movements
          elif event.key == pygame.K_DOWN:
            offset_y -= buttons_movements
        
        # --- Zooming (Mouse) ---
        
        # Mouse Wheel
        elif event.type == pygame.MOUSEWHEEL:
          if event.y > 0: # scroll up
            zoom = min(zoom_range[0], zoom * 1.1)
          elif event.y < 0: # scroll down
            zoom = max(zoom_range[1], zoom / 1.1)

        # --- Screen Movements (Mouse) ---
        
        # Mouse Drag
        # start
        elif event.type == pygame.MOUSEBUTTONDOWN:
          # Press button zooming
          if zoom_in_button.collidepoint(mouse_pos):
            zoom = min(zoom_range[0], zoom * 1.1)
          elif zoom_out_button.collidepoint(mouse_pos):
            zoom = max(zoom_range[1], zoom / 1.1)
          elif reverse_button.collidepoint(mouse_pos):
            print("EEEE")
            for var in last_station_pressed:
              print(var)
            if last_station_pressed:
              last = last_station_pressed.pop()
              station_opened[last] = False
              print(last)
          elif all_trains_button.collidepoint(mouse_pos):
            train_page()
          elif rezoom_button.collidepoint(mouse_pos):
            zoom = 1.0
            # offset_x, offset_y = -(width // 100000), -(height // 100)
            offset_x, offset_y = 450, 0
            dragging = False
            last_mouse_pos = (0, 0)
          else:
            # for name in station_name:
            #   if station_opened[name]:
            #     pos = transform(stations_pos[name])
            #     r = int(station_circle_radius * zoom)
            #     dx = mouse_pos[0] - pos[0]
            #     dy = mouse_pos[1] - pos[1]
            #     if dx * dx + dy * dy <= r * r:
            #       last_station_pressed.append(name)
            #       print(f"Station name: {name}")
            #       print("E")
            #       break
            #     for branch in (stations_branches[name]):
            #       pos_branch = transform(stations_pos[branch])
            #       r_branch = int(station_circle_radius * zoom)
            #       dx_branch = mouse_pos[0] - pos_branch[0]
            #       dy_branch = mouse_pos[1] - pos_branch[1]
            #       if dx_branch * dx_branch + dy_branch * dy_branch <= r_branch * r_branch:
            #         last_station_pressed.append(branch)
            #         # print(f"Station name: {name}")
            #         print(f"Branches: {branch}")
            #         print("Others: ")
            #         for kiu in (stations_branches[branch]):
            #           print(kiu)
            #         station_opened[branch] = True
            #         break

            for name in ordered_stations:
              if station_opened[name]:
                for branch in stations_branches[name]:
                  pos_branch = transform(stations_pos[branch])
                  r_branch = int(station_circle_radius * zoom)
                  dx_branch = mouse_pos[0] - pos_branch[0]
                  dy_branch = mouse_pos[1] - pos_branch[1]
                  if dx_branch * dx_branch + dy_branch * dy_branch <= r_branch * r_branch:
                    station_opened[branch] = True
                    last_station_pressed.append(branch)
                    print(f"Opened branch: {branch}")
                    break
          
            # Mouse move
            if event.button == 1 and not(
              zoom_in_button.collidepoint(mouse_pos) or 
              zoom_out_button.collidepoint(mouse_pos) or 
              reverse_button.collidepoint(mouse_pos) or 
              all_trains_button.collidepoint(mouse_pos) or 
              menu_button.collidepoint(mouse_pos) or 
              rezoom_button.collidepoint(mouse_pos)
            ): # left click
              dragging = True
              last_mouse_pos = event.pos
          
          # elif event.button == 1 and not(zoom_in_button.collidepoint(mouse_pos) or zoom_out_button.collidepoint(mouse_pos)): # left click
          #   dragging = True
          #   last_mouse_pos = event.pos
        
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
