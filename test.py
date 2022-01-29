from de.scripts.windows import *
from de.scripts.simple_pg import *
import numpy as np
import time

def init():
    global node_pos, node_vel, links, size_x, size_y, link_length, stiffness, damping, moved_node, node_size, tolerance, w1

    w1 = Window(np.array([10, 20]), np.array([500, 300]))
    fill((0, 0, 0), w1.surface)

    config.set_max_fps(9999)

    moved_node = (-1, -1)
    link_length = 50
    stiffness = 10
    damping = 0.5
    node_size = 10

    size_x = 2
    size_y = 2

    node_pos = np.array([[[x * link_length, y * link_length] for y in range(size_y)] for x in range(size_x)], dtype=object)
    node_vel = np.array([[[0, 0] for _ in range(size_y)] for _ in range(size_x)], dtype=object)
    links = []

    for x in  range(size_x):
        for y in range(size_y):
            if x > 0:
                links.append(((x, y), (x - 1, y)))
                if y > 0:
                    links.append(((x, y), (x - 1, y - 1)))
                # if y < size_y - 1:
                #     links.append(((x, y), (x + -1, y + 1)))
            if y > 0:
                links.append(((x, y), (x, y - 1)))

def events(event: pygame.event.Event):
    global node_pos, node_vel, links, size_x, size_y, link_length, stiffness, damping, moved_node, node_size, w1

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = np.array(pygame.mouse.get_pos()) - w1.pos
        closest_node_distance = math.inf
        for x in range(len(node_pos)):
            for y in range(len(node_pos[x])):
                diff = node_pos[x][y] - mouse_pos
                distance = abs(math.sqrt(diff[0]**2 + diff[1]**2))
                if distance < closest_node_distance and distance < node_size:
                    closest_node_distance = distance
                    moved_node = (x, y)
    if event.type == pygame.MOUSEBUTTONUP:
        moved_node = (-1, -1)

def tick(delta):
    global node_pos, node_vel, links, size_x, size_y, link_length, stiffness, damping, moved_node, node_size, w1

    vel_multiplier = 1 / (damping + 1)
    for i in range(20):
        for link in links:
            a = node_pos[int(link[0][0])][int(link[0][1])]
            b = node_pos[int(link[1][0])][int(link[1][1])]

            vel_a = node_vel[int(link[0][0])][int(link[0][1])]
            vel_b = node_vel[int(link[1][0])][int(link[1][1])]

            diff = b - a

            streched_length = math.sqrt(diff[0]**2 + diff[1]**2)
            strech_distance = streched_length - link_length

            force = stiffness * strech_distance * delta
            if diff[0] > 0:
                angle = math.atan(diff[1] / diff[0])
            elif diff[0] < 0:
                angle = -math.pi - math.atan(-diff[1] / diff[0])
            else:
                angle = 0
            directed_force = np.array([math.cos(angle) * force, math.sin(angle) * force]) * delta

            vel_a += directed_force
            vel_b -= directed_force


        if moved_node != (-1, -1):
            mouse_pos = np.array(pygame.mouse.get_pos()) - w1.pos
            node_pos[int(moved_node[0])][int(moved_node[1])][0] = mouse_pos[0]
            node_pos[int(moved_node[0])][int(moved_node[1])][1] = mouse_pos[1]
            node_vel[int(moved_node[0])][int(moved_node[1])][0] = 0
            node_vel[int(moved_node[0])][int(moved_node[1])][1] = 0

        node_vel *= vel_multiplier**delta

        node_pos += delta * node_vel

def draw():
    global node_pos, node_vel, links, size_x, size_y, link_length, stiffness, damping, w1
    fill((255, 255, 255), w1.surface)
    outline_points = []
    for x in range(size_x):
        outline_points.append(node_pos[x][0])
    for y in range(1, size_y):
        outline_points.append(node_pos[size_x - 1][y])
    for x in range(2, size_x):
        outline_points.append(node_pos[size_x - x][size_y - 1])
    for y in range(1, size_y):
        outline_points.append(node_pos[0][ size_y - y])

    # polygon(outline_points, (0, 0, 0))
    
    for x in range(len(node_pos)):
        for y in range(len(node_pos[x])):
            circle(node_pos[x][y][0], node_pos[x][y][1], node_size, (0, 0, 0), surface = w1.surface)
    for nodes in links:
        pos1 = node_pos[nodes[0][0]][nodes[0][1]]
        pos2 = node_pos[nodes[1][0]][nodes[1][1]]
        line(pos1[0], pos1[1], pos2[0], pos2[1], (0, 0, 0), surface = w1.surface)
