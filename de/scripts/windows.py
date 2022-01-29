import numpy as np
import pygame
from de.scripts.de_lib import *

class Window(object):
    all: 'list[Window]' = []

    def __init__(self, pos: np.ndarray = None, size: np.ndarray = None): 
        Window.all.append(self)
        if pos is None:
            pos = np.array([0, 0], dtype=np.int32)
        if size is None:
            size = np.array([0, 0], dtype=np.int32)
        self.pos: np.ndarray = pos
        self.size: np.ndarray = size
        self.surface: pygame.Surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.header_size = config.configs['Window']['Header']['Default_Size']
    
    def set_size(self, size: np.ndarray):
        self.size = size
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)