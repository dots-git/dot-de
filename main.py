# This opens the desktop environment
from importlib import import_module
from de.scripts.simple_pg import *
from de.scripts.windows import *

def init():
    global moved_window, moving_offset, test, active_window
    test = [import_module('test'), import_module('demos.tetris_ui')]
    config.load()
    for t in test:
        t.init()
    moved_window = None
    active_window = None
    moving_offset = np.array([0, 0])

def events(event):
    global moved_window, moving_offset, test, active_window
    is_pressed = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            if is_pressed[pygame.K_LCTRL] or is_pressed[pygame.K_RCTRL]:
                print("Quitting")
                return False
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

def tick(delta):
    global moved_window, moving_offset, test, active_window
    for t in test:
        t.tick(delta)
    mouse_pos = pygame.mouse.get_pos()
    if not (moved_window is None):
        moved_window.pos = np.array([mouse_pos[0],mouse_pos[1]]) + moving_offset

def draw():
    global moved_window, moving_offset, test, active_window
    for t in test:
        t.draw()
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


go(init, events, tick, draw, 0, 0)