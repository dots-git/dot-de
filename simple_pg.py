import pygame
from pygame import gfxdraw
import time
import math

def size(surface: pygame.Surface = None):
    ''' 
    Returns a tuple of the width and height of the window 
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    return surface.get_size()

def width(surface: pygame.Surface = None):
    ''' 
    Returns the width of the window 
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    return surface.get_size()[0]

def height(surface: pygame.Surface = None):
    ''' 
    Returns the height of the window 
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    return surface.get_size()[1]

def circle(x: 'int | float', y: 'int | float', r: 'int | float', color, filled: bool = True, surface: pygame.Surface = None):
    ''' 
    Draw an antialiased circle 
    
    :param x: The x coordinate of the circle's center
    :param y: The y coordinate of the circle's center
    :param r: The radius of the circle
    :param color: The color of the circle
    :param filled: Whether or not the circle should be filled
    :param surface: The surface to draw the circle on
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    if filled:
        s = pygame.Surface([2 * r + 1, 2 * r + 1], pygame.SRCALPHA)
        for i in range(2 * r + 1):
            for j in range(2 * r + 1):
                distance = math.sqrt((i - r)**2 + (j - r)**2)
                alpha = 255
                if distance > r + 1:
                    alpha = 0
                elif distance > r:
                    alpha = -255 * distance + 255 * (r + 1)
                s.set_at((i, j), (color[0], color[1], color[2], alpha))
        surface.blit(s, (x, y))
    else:
        gfxdraw.aacircle(surface, int(x), int(y), int(r), color)

def line(x1: 'int | float', y1: 'int | float', x2: 'int | float', y2: 'int | float', color, surface: pygame.Surface = None):
    ''' 
    Draw an antialiased line 
    
    :param x1: The x coordinate of point 1 of the line
    :param y1: The y coordinate of point 1 of the line
    :param x2: The x coordinate of point 2 of the line
    :param y2: The y coordinate of point 2 of the line
    :param color: The color of the line
    :param surface: The surface to draw the line on
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
    :param surface: The surface to draw the polygon on
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    gfxdraw.aapolygon(surface, points, color)
    if filled:
        pygame.draw.polygon(surface, color, points)

def rectangle(x: 'float | int', y: 'float | int', width: 'float | int', height: 'float | int', color, outline: 'float | int' = 0, surface: pygame.Surface = None):
    ''' 
    Draw an axis-aligned rectangle. 
    
    :param x: The x coordinate of the rectangle
    :param y: The y coordinate of the rectangle
    :param width: The width of the rectangle
    :param height: The height of the rectangle
    :param color: The color of the rectangle
    :param outline: Width of the rectangle's outline. 0 for a filled rectangle
    :param surface: The surface to draw the rectangle on
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, rect, outline)

def rounded_rectangle(x: 'float | int', y: 'float | int', width: 'float | int', height: 'float | int', color, radius: 'float | int', surface: pygame.Surface = None):
    '''
    Draw a rounded rectangle

    :param x: The x coordinate of the rectangle
    :param y: The y coordinate of the rectangle
    :param width: The width of the rectangle 
    :param height: The height of the rectangle
    :param color: The color of the rectangle
    :param radius: The corner radius of the rectangle
    :param surface: The surface to draw the rectangle on
    '''
    if surface is None:
        surface = pygame.display.get_surface()

    if radius * 2 > width:
        radius = width / 2 - 1
    if radius * 2 > height:
        radius = height / 2 - 1

    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill(color)
    surface.blit(rounded(s, radius), (x, y))

def image(x, y, image, surface: pygame.Surface = None):
    '''
    Draw an image on the screen

    :param x: The x coordinate of the image
    :param y: The y coordinate of the image
    :param surface: The surface to draw the image on

    '''

    if surface is None:
        surface = pygame.display.get_surface()
    
    surface.blit(image, (x, y))

def fill(color, surface: pygame.Surface = None):
    ''' 
    Fill the canvas with the given color

    :param color: The color to fill the canvas with    
    '''
    if surface is None:
        surface = pygame.display.get_surface()
    surface.fill(color)

def rounded(surface: pygame.Surface, radius, rounded_corners: 'list[bool]' = [True, True, True, True]):
    rounded_surface = surface.copy()


    for i in range(radius):
        for j in range(radius):
            x = 0
            y = 0
            
            distance = math.sqrt((radius - i)**2 + (radius - j)**2)
            alpha = 255
            if distance > radius + 1:
                alpha = 0
            elif distance > radius:
                alpha = -255 * distance + 255 * (radius + 1)
            for k in range(4):
                if rounded_corners[k]:
                    if k == 0:
                        x = i
                        y = j
                    elif k == 1:
                        x = rounded_surface.get_size()[0] - i - 1
                        y = j
                    elif k == 2:
                        x = i   
                        y = rounded_surface.get_size()[1] - j - 1
                    elif k == 3:
                        x = rounded_surface.get_size()[0] - i - 1
                        y = rounded_surface.get_size()[1] - j - 1
                    color = rounded_surface.get_at((x, y))
                    color = (color[0], color[1], color[2], alpha)
                    rounded_surface.set_at((x, y), color)
    return rounded_surface

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
    screen = None
    if width == 0:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
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
            if events_fuc(event) == False:
                running = False
        

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