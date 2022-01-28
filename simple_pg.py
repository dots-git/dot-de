import pygame
from pygame import gfxdraw
import time
import sys

def size(surface: pygame.Surface = None):
    ''' 
    Returns a tuple of the width and height of the window 
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    return surface.get_size()

def circle(x: 'int | float', y: 'int | float', r: 'int | float', color, filled: bool = True, surface: pygame.Surface = None):
    ''' 
    Draw an antialiased circle 
    
    :param x: The x coordinate of the circle's center
    :param y: The y coordinate of the circle's center
    :param r: The radius of the circle
    :param color: The color of the circle
    :param filled: Whether or not the circle should be filled
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    gfxdraw.aacircle(surface, int(x), int(y), int(r), color)
    if filled:
        if r > 1:
            gfxdraw.aacircle(surface, int(x), int(y), int(r) - 1, color)
        pygame.draw.circle(surface, color, (int(x) + 1, int(y)), int(r))

def line(x1: 'int | float', y1: 'int | float', x2: 'int | float', y2: 'int | float', color, surface: pygame.Surface = None):
    ''' 
    Draw an antialiased line 
    
    :param x1: The x coordinate of point 1 of the line
    :param y1: The y coordinate of point 1 of the line
    :param x2: The x coordinate of point 2 of the line
    :param y2: The y coordinate of point 2 of the line
    :param color: The color of the line
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    gfxdraw.aapolygon(surface, ((int(x1), int(y1)), (int(x2), int(y2)), (int(x1), int(y1))), color)

def polygon(points, color, filled: bool = True, surface: pygame.Surface = None):
    ''' 
    Draw an antialiased polygon 

    :param points: The list of points of the polygon
    :param color: The color of the polygon
    :param filled: Whether or not the polygon should be filled
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    gfxdraw.aapolygon(surface, points, color)
    if filled:
        pygame.draw.polygon(surface, color, points)

def rectangle(x: 'float | int', y: 'float | int', width: 'float | int', height: 'float | int', color, outline: 'float | int' = 0, surface: pygame.Surface = None):
    ''' 
    Draw an axis-aligned rectangle. Supports rounded corners 
    
    :param x: The x coordinate of the rectangle
    :param y: The y coordinate of the rectangle
    :param width: The width of the rectangle
    :param height: The height of the rectangle
    :param color: The color of the rectangle
    :param outline: Width of the rectangle's outline. 0 for a filled rectangle
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, rect, outline)

def fill(color, surface: pygame.Surface = None):
    ''' 
    Fill the canvas with the given color

    :param color: The color to fill the canvas with    
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    surface.fill(color)

def init():
    pass

def events(event):
    pass

def tick(delta):
    pass

def draw():
    pass

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class config():
    max_fps = 0
    min_delta = 0
    background_color = WHITE
    fps_update_interval = 0.5
    curr_fps = 0

    @staticmethod
    def set_max_fps(value):
        ''' Change the FPS limit. Exists to save resources '''
        config.max_fps = value
        config.min_delta = 1 / config.max_fps
        config.just_updated = True
    
    @staticmethod
    def set_fps_update_interval(value):
        ''' Change the FPS update interval. Makes FPS displays more readable '''
        config.fps_update_interval = value

config.set_max_fps(65)

def go(init_func = init, events_fuc = events, tick_func = tick, draw_func = draw, width = 1000, height = 600, name = 'New Project'):
    ''' Start the game loop '''
    pygame.init()
    pygame.mixer.init()  ## For sound
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption(name)

    current_time = time.time()
    time_last_frame = current_time
    delta = config.min_delta
    delta_list = []
    fps_display_update_time = config.fps_update_interval

    init_func()
    running = True
    while running:
        for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them. 
            # listening for the the X button at the top
            if event.type == pygame.QUIT:
                running = False
            events_fuc(event)

        tick_func(delta)

        screen.fill(config.background_color)

        draw_func()
        
        pygame.display.flip()   

        current_time = time.time()
        delta = current_time - time_last_frame
        if delta < config.min_delta:
            time.sleep(config.min_delta - delta)
            current_time = time.time()
            delta = current_time - time_last_frame
        time_last_frame = current_time

        if delta == 0:
            delta += 10e-255
        delta_list.append(delta)
        fps_display_update_time -= delta
        


        if fps_display_update_time < 0:
            print("Fps: %i (Min: %i, Max: %i)" % (len(delta_list)/sum(delta_list), 1/max(delta_list), 1/min(delta_list)))
            config.curr_fps = 1 / delta
            delta_list = []
            fps_display_update_time = config.fps_update_interval

    pygame.quit()