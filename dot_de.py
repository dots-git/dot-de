# This opens the desktop environment
from simple_pg import *
from windows import *
import math

def init():
    global surf, moved_window, moving_offset
    w1 = Window(np.array([10, 30]), np.array([100, 100]))
    w1.surface.fill((0, 0, 0, 255))
    moved_window = None
    moving_offset = np.array([0, 0])

def events(event):
    global surf, moved_window, moving_offset
    is_pressed = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            if is_pressed[pygame.K_LCTRL] or is_pressed[pygame.K_RCTRL]:
                print("Quitting")
                return False
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        for i in range(len(Window.all)):
            j = len(Window.all) - i - 1
            if Window.all[j].pos[0] < mouse_pos[0] < Window.all[j].pos[0] + Window.all[j].size[0]:
                if Window.all[j].pos[1] - 20 < mouse_pos[1] < Window.all[j].pos[1]:
                    moved_window = Window.all[j]
                    moving_offset[0] = Window.all[j].pos[0] - mouse_pos[0]
                    moving_offset[1] = Window.all[j].pos[1] - mouse_pos[1]
                    break
    if event.type == pygame.MOUSEBUTTONUP:
        if not (moved_window is None):
            moved_window = None

def tick(delta):
    global surf, moved_window, moving_offset
    mouse_pos = pygame.mouse.get_pos()
    if not (moved_window is None):
        moved_window.pos = np.array([mouse_pos[0],mouse_pos[1]]) + moving_offset

def draw():
    global surf, moved_window
    radius = 10
    offset = 4
    overlap = 10
    height = 28
    button_size = 10
    shadow_radius = 10

    fill((20, 20, 20))

    for win in Window.all:
        rounded_surface = rounded(win.surface, radius)

        shadow = pygame.Surface((win.size[0] + 2*shadow_radius, win.size[1] + 2*shadow_radius))

        rounded_rectangle(win.pos[0] - offset, win.pos[1] - height, win.size[0] + offset * 2, height + overlap, (30, 30, 50), radius)
        circle(win.pos[0] + win.size[0] - button_size * 2 - 2, win.pos[1] - 2*button_size - 3, button_size, (225, 70, 70))
        image(win.pos[0], win.pos[1], rounded_surface)


go(init, events, tick, draw, 0, 0)