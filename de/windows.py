from tkinter import E
import numpy as np
import pygame
from de.os import *
from de.simple_pg import *
from de.animated_rect import *

class Window(object):
    all: 'list[Window]' = []
    types_to_open = []

    @staticmethod
    def open(type_to_open):
        Window.types_to_open.append(type_to_open)

    def __init__(self, x = 0, y = 0, w = 0, h = 0): 
        Window.all.append(self)
        
        self.slomo = 1

        self.has_header: bool = True
        self.rect: AnimatedRect = AnimatedRect(x, y, w, h, 5, 10000, 5)
        self.surface: pygame.Surface = pygame.Surface((w, h), pygame.SRCALPHA)
        self.resizable: bool = False
        self.base_color = WHITE
        self.draw_by_default: bool = True

        self.move_to_front = True
        self.is_still = False

        configs: dict[ConfValue] = os.configs['Window']['Header']
        self.header_width: int = configs['Width'].get()
        self.header_height: int = configs['Height'].get() if self.has_header else 0
        self.header_offset: int = configs['Vertical offset'].get()
        self.header_color: pygame.Color = configs['Color'].get()
        self.header = AnimatedRect(
            self.x() - self.header_width / 2, 
            self.y() - self.header_height + self.header_offset, 
            self.width() + self.header_width, 
            self.header_height,
            5,
            10000,
            5
        )
        self.window_radius = os.configs['Window']['Corner radius'].get()

        self.init()

        self.tick(10e-255)
        self.window_tick(10e-255)

    def quit(self):
        Window.all.remove(self)

    def set_has_header(self, value):
        self.has_header = value
        self.header_height: int = os.configs['Window']['Header']['Height'].get() if self.has_header else 0


    def set_size(self, w, h, animate = False):
        self.width(w, animate)
        self.height(h, animate)
    
    def set_pos(self, x, y, animate = False):
        if animate:
            self.x(x, True)
            self.y(y, True)
        else:
            self.x(x)
            self.y(y)
    
    def mouse_pos(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return (mouse_x - self.x(), mouse_y - self.y())

    def window_tick(self, delta):
        surface_size = (int(self.rect.get_width()), int(self.rect.get_height()))
        self.rect.animate(delta * self.slomo)
        if self.surface.get_size() != surface_size:
            self.surface = pygame.Surface(surface_size, pygame.SRCALPHA)
        if self.has_header:
            if self.header.animate(delta * self.slomo):
                self.header_surface = pygame.Surface

    def draw_window(self):
        if self.has_header:
            rounded_rectangle(self.header.get_x(), self.header.get_y(), self.header.get_width(), self.header.get_height(), self.header_color, self.window_radius)         
        rounded_surface = rounded(self.surface, self.window_radius)
        image(self.x(), self.y(), rounded_surface)


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
    
    def x(self, x = None, animate = False):
        if x is None:
            return self.rect.get_x()
        else:
            if animate:
                self.header.set_x(x - self.header_width / 2)
                self.rect.set_x(x)
            else:
                self.header.set_x_no_animation(x - self.header_width / 2)
                self.rect.set_x_no_animation(x)
    
    def y(self, y = None, animate = False): 
        if y is None:
            return self.rect.get_y()
        else:
            if animate:
                self.header.set_y(y - self.header_height + self.header_offset)
                self.rect.set_y(y)
            else:
                self.header.set_y_no_animation(y - self.header_height + self.header_offset)
                self.rect.set_y_no_animation(y)

    def width(self, w = None, animate = False):
        ''' 
        Returns the width of the window or sets it if a value is given
        '''
        if w is None:
            return self.rect.get_width()
        else:
            if animate:
                self.header.set_width(w + self.header_width)
                self.rect.set_width(w)
            else:
                self.header.set_width_no_animation(w + self.header_width)
                self.rect.set_width_no_animation(w)

    def height(self, h = None, animate = False):
        ''' 
        Returns the height of the window or sets it if a value is given
        '''
        if h is None:
            return self.rect.get_height()
        else:
            if animate:
                self.header.set_height(self.header_height)
                self.rect.set_height(h)
            else:
                self.header.set_height_no_animation(self.header_height)
                self.rect.set_height_no_animation(h)
    
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
