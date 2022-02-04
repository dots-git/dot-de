from glob import escape
from re import T
import numpy as np
import pygame
from de.os import *
from de.simple_pg import *

class Window(object):
    all: 'list[Window]' = []

    def __init__(self, x = 0, y = 0, w = 0, h = 0, hasHeader = True, resizable = False, base_color = WHITE, draw_by_default = True): 
        Window.all.append(self)
        
        self.hasHeader: bool = hasHeader
        self.pos: np.ndarray = np.asarray([x, y])
        self.size: np.ndarray = np.asarray([w, h])
        self.surface: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.resizable: bool = resizable
        self.base_color = base_color
        self.draw_by_default: bool = draw_by_default

        self.move_to_front = True
        self.init()


        configs: dict[ConfValue] = os.configs['Window']['Header']
        if self.hasHeader:
            header_width: int = configs['Width'].get()
            header_height: int = configs['Height'].get()
            header_offset: int = configs['Vertical offset'].get()
            header_color: pygame.Color = configs['Color'].get()
            self.header = Header(
                self.x() - header_width / 2, 
                self.y() - header_height + header_offset, 
                self.width() + header_width, 
                header_height,
                False,
                base_color = header_color, 
                draw_by_default = False
            )
            self.header_height = header_height - header_offset
        else:
            self.header_height = 0
        self.window_radius = os.configs['Window']['Corner radius'].get()

    def update_header(self):
        configs: dict[ConfValue] = os.configs['Window']['Header']
        if self.hasHeader:
            header_width: int = configs['Width'].get()
            header_height: int = self.header_height
            header_offset: int = configs['Vertical offset'].get()
            self.header.set_pos(
                self.x() - header_width / 2, 
                self.y() - header_height + header_offset
            )
            self.header.set_size(
                self.width() + header_width, 
                header_height
            )

    def quit(self):
        Window.all.remove(self)

    def set_size(self, x, y):
        self.size = np.asarray([x, y])
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
    
    def set_pos(self, x, y):
        self.pos = np.asarray([x, y])
    
    def mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (mouse_x - self.pos[0], mouse_y - self.pos[1])

    def draw_window(self):
        if self.hasHeader:
            self.update_header()
            self.header.draw_window()           
        rounded_surface = rounded(self.surface, self.window_radius)
        image(self.pos[0], self.pos[1], rounded_surface)

    # A bunch of functions to make drawing on the window easier, most just use the functions from simple_pg
    def screen_size(self):
        ''' 
        Returns a tuple of the width and height of the screen 
        '''
        return size()
    
    def screen_width(self):
        '''
        Returns the width of the screen        
        '''
        return width()
    
    def screen_height(self):
        '''
        Returns the height of the screen
        '''
        return height()
    
    def x(self):
        return self.pos[0]
    
    def y(self): 
        return self.pos[1]

    def width(self):
        ''' 
        Returns the width of the window 
        '''
        return self.size[0]
    
    def height(self):
        ''' 
        Returns the height of the window 
        '''
        return self.size[1]
    
    def circle(self, x: 'int | float', y: 'int | float', r: 'int | float', color, filled: bool = True):
        ''' 
        Draw an antialiased circle 
        
        :param x: The x coordinate of the circle's center
        :param y: The y coordinate of the circle's center
        :param r: The radius of the circle
        :param color: The color of the circle
        :param filled: Whether or not the circle should be filled
        '''
        circle(x, y, r, color, filled, self.surface)

    def line(self, x1: 'int | float', y1: 'int | float', x2: 'int | float', y2: 'int | float', color, w = 1):
        ''' 
        Draw an antialiased line 
        
        :param x1: The x coordinate of point 1 of the line
        :param y1: The y coordinate of point 1 of the line
        :param x2: The x coordinate of point 2 of the line
        :param y2: The y coordinate of point 2 of the line
        :param color: The color of the line
        '''
        line(x1, y1, x2, y2, color, w, self.surface)

    def polygon(self, points, color, filled: bool = True, surface: pygame.Surface = None):
        ''' 
        Draw an antialiased polygon 

        :param points: The list of points of the polygon
        :param color: The color of the polygon
        :param filled: Whether or not the polygon should be filled
        :param surface: The surface to draw the polygon on
        '''
        polygon(points, color, filled, self.surface)

    def rectangle(self, x: 'float | int', y: 'float | int', width: 'float | int', height: 'float | int', color, outline: 'float | int' = 0):
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
        rectangle(x, y, width, height, color, outline, self.surface)

    def rounded_rectangle(self, x: 'float | int', y: 'float | int', width: 'float | int', height: 'float | int', color, radius: 'float | int'):
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
        rounded_rectangle(x, y, width, height, color, radius, self.surface)

    def image(self, x, y, img):
        '''
        Draw an image on the screen

        :param x: The x coordinate of the image
        :param y: The y coordinate of the image
        :param surface: The surface to draw the image on

        '''
        image(x, y, img, self.surface)

    def text(self, x: int, y: int, text_str: str, color: pygame.draw, font: str = 'Linux Biolinum G', font_size: int = 30, bold: bool = False, italic: bool = False, alignment_x: str = 'center', alignment_y: str = 'center'):
        '''
        Draw text on the screen

        :param x: The x coordinate of the text origin
        :param y: The y coordinate of the text origin
        :param text: The text to draw
        :param font: The font to draw the text in
        :param font_size: The font size of the text
        :param color: The color to draw the text in
        :param alignment_x: The horizontal alignment of the text ('left', 'center' or 'right')
        :param alignment_y: The vertical alignment of the text ('top', 'center' or 'bottom')
        :param surface: The surface to draw the text on
        '''
        text(x, y, text_str, color, font, font_size, bold, italic, alignment_x, alignment_y, self.surface)
        

    def fill(self, color):
        ''' 
        Fill the canvas with the given color

        :param color: The color to fill the canvas with    
        '''
        self.surface.fill(color)


    def init(self):
        pass

    def events(self, event):
        pass

    def tick(self, delta):
        pass

    def draw(self):
        pass

class Header(Window):
    def draw(self):
        pass