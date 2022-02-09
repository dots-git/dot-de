from de.animated_rect import *
from de.simple_pg import *

def init():
    global my_rect, draw_starting_point, drawing, radius

    my_rect = AnimatedRect(0, 0, width(), height(), 10, 1000, 7, 0)

    my_rect.set_y(100)
    my_rect.set_x(0)
    my_rect.set_width(150)
    my_rect.set_height(40)
    
    draw_starting_point = (0, 0)
    drawing = False
    radius = 0

def events(event):
    global draw_starting_point, drawing

    if event.type == pygame.MOUSEBUTTONDOWN:
        drawing = True
        draw_starting_point = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONUP:
        drawing = False
        draw_ending_point = pygame.mouse.get_pos()
        top = min(draw_starting_point[1], draw_ending_point[1])
        bottom = max(draw_starting_point[1], draw_ending_point[1])
        left = min(draw_starting_point[0], draw_ending_point[0])
        right = max(draw_starting_point[0], draw_ending_point[0])
        my_rect.set_pos(left, top)
        my_rect.set_width(right - left)
        my_rect.set_height(bottom - top)

def tick(delta):
    my_rect.animate(delta)  
    mouse_x, mouse_y = pygame.mouse.get_pos()  
    my_rect.set_pos(mouse_x, mouse_y)

def draw():
    if not drawing:
        rounded_rectangle(int(my_rect.target_vector[0]), int(my_rect.target_vector[1]), int(my_rect.target_vector[2]), int(my_rect.target_vector[3]), (180, 180, 180), radius)

    rounded_rectangle(my_rect.get_x(), my_rect.get_y(), my_rect.get_width(), my_rect.get_height(), (0, 0, 0), radius)
    if drawing:
        draw_ending_point = pygame.mouse.get_pos()
        top = min(draw_starting_point[1], draw_ending_point[1])
        bottom = max(draw_starting_point[1], draw_ending_point[1])
        left = min(draw_starting_point[0], draw_ending_point[0])
        right = max(draw_starting_point[0], draw_ending_point[0])
        rounded_rectangle(left, top, right - left, bottom - top, (180, 180, 180), radius)

go(init, events, tick, draw)