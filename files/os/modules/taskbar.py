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
        self.set_has_header(False)
        self.base_color = (60, 80, 100)

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
    
    def events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("MOUSEBUTTONDOWN")
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.y() < mouse_y < self.y() + self.height():
                for i in range(len(self.shortcuts)):
                    print(i)
                    if self.max_taskbar_height * i < mouse_x < self.max_taskbar_height * (i + 1):
                        if 'script' in self.shortcuts[i].keys():
                            os.run_script(self.shortcuts[i]['script'][0], self.max_taskbar_height * (i + self.icon_padding), self.y() + self.taskbar_height * self.icon_padding, self.taskbar_height * (1 - 2 * self.icon_padding), self.taskbar_height * (1 - 2 * self.icon_padding))


    def draw(self):
        for i in range(len(self.shortcuts)):
            self.image(self.max_taskbar_height * (i + self.icon_padding), self.taskbar_height * self.icon_padding, self.shortcuts[i]['icon'])


Window.open(TaskbarWindow)

