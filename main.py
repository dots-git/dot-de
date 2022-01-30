import pygame
import time
import numpy as np
from de.scripts.simple_pg import *
from de.scripts.de_lib import *
from de.scripts.windows import *

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class win_config():
    max_fps = 0
    min_delta = 0
    background_color = WHITE
    fps_update_interval = 0.5
    curr_fps = 0

    @staticmethod
    def set_max_fps(value):
        ''' Change the FPS limit. Exists to save resources '''
        win_config.max_fps = value
        win_config.min_delta = 1 / win_config.max_fps
        win_config.just_updated = True
    
    @staticmethod
    def set_fps_update_interval(value):
        ''' Change the FPS update interval. Makes FPS displays more readable '''
        win_config.fps_update_interval = value

def open_file(filename):
    exec(open(filename).read())

win_config.set_max_fps(65)

''' Start the game loop '''
pygame.init()
pygame.mixer.init()  ## For sound
screen = None
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('dotOS Proof of Concept')

current_time = time.time()
time_last_frame = current_time
delta = win_config.min_delta
delta_list = []
fps_display_update_time = win_config.fps_update_interval

config.load()

files_to_run = []
files_to_run.append('./demos/fabric_sim.py')
files_to_run.append('./demos/tetris_ui.py')

moved_window = None
active_window = None
moving_offset = np.array([0, 0])

running = True
while running:
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them. 
        # listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False
        is_pressed = pygame.key.get_pressed()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if is_pressed[pygame.K_LCTRL] or is_pressed[pygame.K_RCTRL]:
                    print("Quitting")
                    running = False
                else:
                    if active_window is not None:
                        active_window.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            active_window = None
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(Window.all)):
                j = len(Window.all) - i - 1
                
                header_height = Window.all[j].header_height

                if Window.all[j].pos[0] < mouse_pos[0] < Window.all[j].pos[0] + Window.all[j].size[0]:
                    found = False
                    if Window.all[j].pos[1] - header_height < mouse_pos[1] < Window.all[j].pos[1]:
                        moved_window = Window.all[j]
                        moving_offset[0] = Window.all[j].pos[0] - mouse_pos[0]
                        moving_offset[1] = Window.all[j].pos[1] - mouse_pos[1]
                        found = True
                    if Window.all[j].pos[1] - header_height < mouse_pos[1] < Window.all[j].pos[1] + Window.all[j].size[1]:
                        print("Active window set")
                        active_window = Window.all[j]
                        for k in range(j, len(Window.all) - 1):
                            tmp = Window.all[k]
                            Window.all[k] = Window.all[k + 1]
                            Window.all[k + 1] = tmp
                        found = True
                    if found:
                        break
        if event.type == pygame.MOUSEBUTTONUP:
            if not (moved_window is None):
                moved_window = None
        for w in Window.all:
            if w == active_window:
                w.events(event)
        

    for w in Window.all:
        w.tick(delta)
    mouse_pos = pygame.mouse.get_pos()
    if not (moved_window is None):
        moved_window.pos = np.array([mouse_pos[0],mouse_pos[1]]) + moving_offset
    
    # Run requested files
    for f in files_to_run:
        exec(open(f).read())
    files_to_run = []

    screen.fill(win_config.background_color)

    for w in Window.all:
        w.fill((255, 255, 255))
        w.draw()
    radius = 10
    offset = 4
    overlap = 10
    button_size = 10
    shadow_radius = 10

    fill((20, 20, 20))

    for win in Window.all:
        header_height = win.header_height

        rounded_surface = rounded(win.surface, radius)

        shadow = pygame.Surface((win.size[0] + 2*shadow_radius, win.size[1] + 2*shadow_radius))

        rounded_rectangle(win.pos[0] - offset, win.pos[1] - header_height, win.size[0] + offset * 2, header_height + overlap, (30, 30, 50), radius)
        circle(win.pos[0] + win.size[0] - button_size * 2 - 2, win.pos[1] - 2*button_size, button_size, (225, 70, 70))
        image(win.pos[0], win.pos[1], rounded_surface)
    
    pygame.display.flip()   

    current_time = time.time()
    delta = current_time - time_last_frame
    if delta < win_config.min_delta:
        time.sleep(win_config.min_delta - delta)
        current_time = time.time()
        delta = current_time - time_last_frame
    time_last_frame = current_time

    if delta == 0:
        delta += 10e-255
    delta_list.append(delta)
    fps_display_update_time -= delta
    


    if fps_display_update_time < 0:
        print("Fps: %i (Min: %i, Max: %i)" % (len(delta_list)/sum(delta_list), 1/max(delta_list), 1/min(delta_list)))
        win_config.curr_fps = 1 / delta
        delta_list = []
        fps_display_update_time = win_config.fps_update_interval

pygame.quit()