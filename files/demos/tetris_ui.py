# adjust_imports
from tetris import *
from de.simple_pg import *
from de.windows import *
from color_manager import *

class TetrisWindow(Window):
    def draw_tetris_square(self, x, y, width, color):
        hsv_rep = hsv(color)
        highlight_color = rgb(hsv_rep[0], hsv_rep[1] * 0.3, hsv_rep[2] + (1 - hsv_rep[2]) * 0.3)
        shadow_color = rgb(hsv_rep[0], hsv_rep[1] * 0.8, hsv_rep[2] * 0.45)
        self.rectangle(x, y, width, width, shadow_color)
        self.rectangle(x, y, width * 0.85, width * 0.85, color)
        self.rectangle(x + width * 0.1, y + width * 0.1, width * 0.15, width * 0.6, highlight_color)
        self.rectangle(x + width * 0.1, y + width * 0.1, width * 0.6, width * 0.15, highlight_color)
    
    def init(self):
        self.game = Game(Vector2(10, 20))
        self.drop_speed = 0.3
        self.time_until_drop = self.drop_speed
        self.drop_accelerator = 1
        self.paused = False

    def events(self, event: pygame.event.Event):
        if not self.paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game.move_left()
                if event.key == pygame.K_RIGHT:
                    self.game.move_right()
                if event.key == pygame.K_DOWN:
                    self.drop_accelerator = 3
                    self.time_until_drop -= self.drop_speed - self.drop_speed / self.drop_accelerator
                if event.key == pygame.K_UP:
                    self.game.rotate_cw()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.drop_accelerator = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused


    def tick(self, delta):
        if not self.paused:
            self.time_until_drop -= delta
            if self.time_until_drop < 0:
                self.game.move_down()
                self.time_until_drop = self.drop_speed / self.drop_accelerator
                rows_cleared = self.game.clear_full_rows()
                if rows_cleared > 0:
                    print(rows_cleared)

    def draw(self):
        joined_array = self.game.get_full_array()
        self.rectangle(25, 25, 300, 600, tetr.color[0])
        for x in range(len(joined_array)):
            for y in range(len(joined_array[x]) - 4):
                if joined_array[x][y + 4] != 0:
                    self.draw_tetris_square(25 + x * 30, 25 + y * 30, 30, tetr.color[joined_array[x][y + 4]])
        if self.paused:
            self.rectangle(10, 10, 20, 50, (180, 180, 200))
            self.rectangle(40, 10, 20, 50, (180, 180, 200))

TetrisWindow(0, 20, 350, 650)
