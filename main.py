import pygame
import time
import numpy as np
from de.os import *
from de.simple_pg import *
from de.windows import *
from de.file_utils import *

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

os.load_configs()
os.run_script('/demos/tetris_launcher.py')
os.run_script('/os/modules/taskbar.py')

moved_window = None
active_window = None
moving_offset = np.array([0, 0])

running = True
while running:
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them. 
        # listening for the the X button at the top
        clicked_header = False
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
                    if Window.all[j].pos[1] - header_height < mouse_pos[1] < Window.all[j].pos[1] and Window.all[j].hasHeader:
                        moved_window = Window.all[j]
                        moving_offset[0] = Window.all[j].pos[0] - mouse_pos[0]
                        moving_offset[1] = Window.all[j].pos[1] - mouse_pos[1]
                        found = True
                        clicked_header = True
                    if Window.all[j].pos[1] - header_height < mouse_pos[1] < Window.all[j].pos[1] + Window.all[j].size[1]:
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
            if w == active_window and not clicked_header:
                w.events(event)
        clicked_header = False
    
    if active_window is not None and not active_window in Window.all:
        active_window = None

    for w in Window.all:
        w.tick(delta)
    mouse_pos = pygame.mouse.get_pos()
    if not (moved_window is None):
        moved_window.pos = np.array([mouse_pos[0],mouse_pos[1]]) + moving_offset
    
    # Run requested files
    for f in os.files_to_run:
        file_content = open(f).read()
        # Adjusting import statements to include paths from rootS
        if file_content[0:17] == '# adjust_imports\n':
            pointer = 17
            imports_over = False
            while not imports_over:
                line = ""
                while not file_content[pointer] == '\n':
                    line += file_content[pointer]
                    pointer += 1
                try:
                    exec(line)
                except ImportError:
                    file_import_path = local_file_location(f)
                    file_import_path = file_import_path.replace('\\', '.').replace('/', '.')
                    words = line.split(' ')
                    for i in range(len(words)):
                        if words[i] != 'import' and words[i] != 'from':
                            if words[0] == 'import' and words[len(words)-2] != 'as':
                                words.append('as ' + words[i])
                            words[i] = 'files' + file_import_path + '.' + words[i]
                            break
                    line = "".join((words[i] + ' ') for i in range(len(words)))
                    exec(line)
                pointer += 1
                if file_content[pointer:pointer+6] != 'import' and file_content[pointer:pointer+4] != 'from':
                    imports_over = True
            exec(file_content[pointer:len(file_content)])
        else:
            exec(file_content)
    os.files_to_run = []


    for w in Window.all:
        if w.pos[1] < w.header_height - w.header_offset:
            w.pos[1] = w.header_height - w.header_offset
        if w.move_to_front:
            active_window = w
            j = Window.all.index(w)
            for k in range(j, len(Window.all) - 1):
                tmp = Window.all[k]
                Window.all[k] = Window.all[k + 1]
                Window.all[k + 1] = tmp
            w.move_to_front = False

    screen.fill(win_config.background_color)

    for w in Window.all:
        w.fill(w.base_color)
        w.draw()
    radius = 10
    offset = 4
    overlap = 10
    button_size = 10
    shadow_radius = 10

    fill((20, 20, 20))

    for w in Window.all:
        w.draw_window()
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