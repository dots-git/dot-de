from pygame import Vector2
from random import randint, shuffle
import numpy as np
from pynput import keyboard

class tetr():
    I = 1
    O = 2
    T = 3
    S = 4
    Z = 5
    J = 6
    L = 7

    array_rep = [
        [
            []
        ],
        [
            [0, I, 0, 0],
            [0, I, 0, 0],
            [0, I, 0, 0],
            [0, I, 0, 0]
        ],
        [
            [O, O],
            [O, O]
        ],
        [
            [0, T, 0],
            [T, T, 0],
            [0, T, 0]
        ],
        [
            [0, S, 0],
            [S, S, 0],
            [S, 0, 0]
        ],
        [
            [Z, 0, 0],
            [Z, Z, 0],
            [0, Z, 0]
        ],
        [
            [J, J, 0],
            [0, J, 0],
            [0, J, 0]
        ],
        [
            [0, L, 0],
            [0, L, 0],
            [L, L, 0]
        ]
    ]

    color = {
        0: (20, 20, 20),
        I: (0, 175, 255),
        O: (255, 255, 0),
        T: (125, 0, 255),
        S: (0, 255, 0),
        Z: (255, 0, 0),
        J: (0, 0, 255),
        L: (255, 125, 0)
    }

print("Defining Game class")
class Game():
    def __init__(self, scale: Vector2):
        self.screen_array = [[0 for _ in range(int(scale.y + 4))] for _ in range(int(scale.x))] 
        self.next_tetromino_id = randint(1, 7)
        self.next_tetromino_bag: list = tetr.array_rep[1:8].copy()
        shuffle(self.next_tetromino_bag)
        self.moving_tetromino = tetr.array_rep[randint(1, 7)]
        self.moving_tetr_pos = Vector2(0, 0)
    
    def is_colliding(self, tetromino: 'list[list[int]]', position: Vector2):
        for i in range(len(tetromino)):
            for j in range(len(tetromino[0])):
                if tetromino[i][j] > 0:
                    if i + position.x < 0:
                        return True
                    if i + position.x >= len(self.screen_array):
                        return True
                    if j + position.y >= len(self.screen_array[0]):
                        return True
                    if self.screen_array[int(i + position.x)][int(j + position.y)] != 0:
                        return True
        return False

    def get_full_array(self):
        return_array = np.array(self.screen_array).copy()
        for i in range(len(self.moving_tetromino)):
            for j in range(len(self.moving_tetromino[0])):
                if self.moving_tetromino[i][j] > 0:
                    return_array[int(i + self.moving_tetr_pos.x)][int(j + self.moving_tetr_pos.y)] = self.moving_tetromino[i][j]
        return return_array

    def move_right(self):
        if not self.is_colliding(self.moving_tetromino, self.moving_tetr_pos + Vector2(1, 0)):
            self.moving_tetr_pos += Vector2(1, 0)
            return True
        return False
    
    def move_left(self):
        if not self.is_colliding(self.moving_tetromino, self.moving_tetr_pos - Vector2(1, 0)):
            self.moving_tetr_pos -= Vector2(1, 0)	
            return True
        return False

    def move_down(self):
        if not self.is_colliding(self.moving_tetromino, self.moving_tetr_pos + Vector2(0, 1)):
            self.moving_tetr_pos += Vector2(0, 1)
        else:
            for i in range(len(self.moving_tetromino)):
                for j in range(len(self.moving_tetromino[0])):
                    if self.moving_tetromino[i][j] != 0:
                        if self.moving_tetr_pos.y + j < 4:
                            self.__init__(Vector2(len(self.screen_array), len(self.screen_array[0]) - 4))
                            return
                        self.screen_array[int(i + self.moving_tetr_pos.x)][int(j + self.moving_tetr_pos.y)] = self.moving_tetromino[i][j]
            self.moving_tetr_pos = Vector2(0, 0)
            if len(self.next_tetromino_bag) == 0:
                self.next_tetromino_bag: list = tetr.array_rep[1:8].copy()
                shuffle(self.next_tetromino_bag)
            self.moving_tetromino = self.next_tetromino_bag[0]
            self.next_tetromino_bag.remove(self.next_tetromino_bag[0])
            print(len(self.next_tetromino_bag))
            

    def clear_full_rows(self):
        rows_cleared = 0
        y1 = 0
        while y1 < len(self.screen_array[0]):
            y1_r = len(self.screen_array[0]) - y1 - 1
            row_is_full = True
            for x1 in range(len(self.screen_array)):
                if self.screen_array[x1][y1_r] == 0:
                    row_is_full = False
                    break
            
            if row_is_full:
                rows_cleared += 1
                for y2 in range(y1, len(self.screen_array[0]) - 1):
                    y2_r = len(self.screen_array[0]) - y2 - 1
                    for x2 in range(len(self.screen_array)):
                        self.screen_array[x2][y2_r] = self.screen_array[x2][y2_r - 1]
                y1 -= 1
            y1 += 1
        return rows_cleared
                



    def rotate_cw(self):
        rotated_tetromino = rotate_cw(self.moving_tetromino)
        if not self.is_colliding(rotated_tetromino, self.moving_tetr_pos):
            self.moving_tetromino = rotated_tetromino
            return True
        return False
        
    def rotate_ccw(self):
        rotated_tetromino = rotate_ccw(self.moving_tetromino)
        if not self.is_colliding(rotated_tetromino, self.moving_tetr_pos):
            self.moving_tetromino = rotated_tetromino
            return True
        return False

    def __str__(self):
        joined_array = self.get_full_array()
        output = '_' * (3 * len(joined_array) + 2) + '\n|'
        for i in range(len(joined_array[0])):
            for j in range(len(joined_array)):
                if joined_array[j][i] > 0:
                    output += '[{}]'.format(joined_array[j][i])
                else:
                    output += '   '
            output += '|\n|'
        return output

            
def rotate_cw(a: 'list[list]') -> 'list[list]':
    b = [[0 for _ in range(len(a))] for _ in range(len(a[0]))]

    for i in range(len(a)):
        for j in range(len(a[i])):
            b[j][len(a) - i - 1] = a[i][j]
    return b

def rotate_ccw(a: 'list[list]') -> 'list[list]':
    b = [[0 for _ in range(len(a))] for _ in range(len(a[0]))]

    for i in range(len(a)):
        for j in range(len(a[i])):
            b[len(a[0]) - j - 1][i] = a[i][j]
    return b

def take_inputs(in_dict):
    while(not in_dict['cancel']):
        with keyboard.Events() as events:
            event = events.get(1e6)
            if event.key == keyboard.Key.esc or event.key == keyboard.KeyCode.from_char('x') or event.key == keyboard.Key.enter:
                in_dict['cancel'] = True
            if event.key == keyboard.Key.right:
                in_dict['right'] = True
            if event.key == keyboard.Key.left:
                in_dict['left'] = True
            if event.key == keyboard.KeyCode.from_char('a'):
                in_dict['rotate_ccw'] = True
            if event.key == keyboard.KeyCode.from_char('d'):
                in_dict['rotate_cw'] = True

input_dict = {
    'cancel': False,
    'left': False,
    'right': False,
    'rotate_ccw': False,
    'rotate_cw': False
}

