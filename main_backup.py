from simple_pg import *
from windows import *
import math

def init():
    global surf
    w1 = Window(np.array([10, 30]), np.array([100, 100]))
    w1.surface.fill((0, 0, 0, 255))

def events(event):
    is_pressed = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            if is_pressed[pygame.K_LCTRL] or is_pressed[pygame.K_RCTRL]:
                print("Quitting")
                return False

def draw():
    global surf
    radius = 10
    offset = 4
    overlap = 10
    height = 28
    for win in Window.all:
        rounded_surface = rounded(win.surface, radius)

        rounded_rectangle(win.pos[0] - offset, win.pos[1] - height, win.size[0] + offset * 2, height + overlap, (30, 30, 50), radius)
        image(win.pos[0], win.pos[1], rounded_surface)

go(init, events, tick, draw, 0, 0)