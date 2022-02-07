from numpy import NAN
from de.anim import *
from de.utils import *
import pygame

class AnimatedRect:
    def __init__(self, x, y, width, height, acceleration, acceleration_modifier, drag):
        self.current_vector = np.array([x, y, width, height], dtype=np.float32)
        self.target_vector = self.current_vector.copy()
        self.velocity_vector = np.zeros(self.current_vector.shape, dtype=np.float32)

        self.acceleration = acceleration
        self.acceleration_modifier = acceleration_modifier
        self.drag = 10**(-drag)
        if self.drag == 0:
            self.drag = 10e-255

    def animate(self, delta):       
        difference_vector: np.ndarray = self.target_vector - self.current_vector
        distance = np.sqrt(difference_vector.dot(difference_vector))
        velocity = np.sqrt(self.velocity_vector.dot(self.velocity_vector))

        velocity = circular_exponential(0, velocity, distance, self.acceleration, self.acceleration_modifier, self.drag, delta)

        if distance > 0:
            direction = difference_vector / distance
        else:
            direction = np.zeros((4, ))
        self.velocity_vector = direction * velocity
        self.current_vector = self.current_vector + self.velocity_vector * delta

        return True
    
    def get_surface(self):
        return pygame.Surface((self.right - self.left, self.bottom - self.top), pygame.SRCALPHA)

    def get_x(self):
        return round(self.current_vector[0])
    
    def get_y(self):
        return round(self.current_vector[1])
    
    def get_width(self):
        w = round(self.current_vector[2])
        return w if w > 0 else 0
    
    def get_height(self):
        h = round(self.current_vector[3])
        return h if h > 0 else 0
    
    def set_x(self, x):
        self.target_vector[0] = x
    
    def set_y(self, y):
        self.target_vector[1] = y

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def set_width(self, width):
        self.target_vector[2] = width
    
    def set_height(self, height):
        self.target_vector[3] = height

    def set_x_no_animation(self, x):
        self.current_vector[0] = x
        self.target_vector[0] = x

    def set_y_no_animation(self, y):
        self.current_vector[1] = y
        self.target_vector[1] = y
    
    def set_width_no_animation(self, width):
        self.current_vector[2] = width
        self.target_vector[2] = width
     
    def set_height_no_animation(self, height):
        self.current_vector[3] = height
        self.target_vector[3] = height
    
    def set_pos_no_animation(self, x, y):
        self.set_x_no_animation(x)
        self.set_y_no_animation(y)
    
    def __str__(self):
        return 'Rect of size %i x %i at x = %i, y = %i' % (self.get_width(), self.get_height(), self.get_x(), self.get_y())