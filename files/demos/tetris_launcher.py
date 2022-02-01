from tkinter import N
from de.windows import *
from de.de_lib import *

class TetrisLauncherWindow(Window):
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = self.mouse_pos()
            print(mouse_x, mouse_y)

            if self.width() * 0.5 - 100 < mouse_x < self.width() * 0.5 + 100 and self.height() * 0.5 - 50 < mouse_y < self.height() * 0.5 + 50:
                config.run_script('/demos/tetris_ui.py')
                print("Running tetris ui script")

    def draw(self):
        self.rounded_rectangle(self.width() * 0.5 - 100, self.height() * 0.5 - 50, 200, 100, (100, 150, 200), 20)
        self.text(self.width() * 0.5, self.height() * 0.5, 'Start Tetris', (255, 255, 255))

w = TetrisLauncherWindow(np.array([400, 20]), np.array([300, 200]))
