# adjust_imports
from parse_sc import *
from de.windows import *
from de.file_utils import *

class TaskbarWindow(Window):
    def init(self):
        self.icon_padding = 0.05
        self.taskbar_height = 40
        self.max_taskbar_height = 40
        self.shortcuts = []
        self.load_shortcuts()

    def load_shortcuts(self):
        f = child_files(files_root() + '/os/taskbar_shortcuts')
        for i in range(len(f)):
            if f[i].endswith('.sc'):
                self.shortcuts.append(sc_to_dict(files_root() + '/os/taskbar_shortcuts/' + f[i]))
                if 'icon' in self.shortcuts[i].keys():
                    self.shortcuts[i]['icon'] = pygame.image.load(files_root() + self.shortcuts[i]['icon'][0])
                else:
                    self.shortcuts[i]['icon'] = pygame.image.load(files_root() + '/os/taskbar_shortcuts/icons/default.png')
                self.shortcuts[i]['icon'] = pygame.transform.smoothscale(self.shortcuts[i]['icon'], (self.taskbar_height * (1 - 2 * self.icon_padding), self.taskbar_height * (1 - 2 * self.icon_padding)))

    def tick(self, delta):
        self.set_size(width(), self.taskbar_height)
        self.set_pos(0, height() - self.taskbar_height)
    
    def draw(self):
        for i in range(len(self.shortcuts)):
            self.image(self.max_taskbar_height * (i + self.icon_padding), self.taskbar_height * self.icon_padding, self.shortcuts[i]['icon'])


TaskbarWindow(hasHeader=False)

