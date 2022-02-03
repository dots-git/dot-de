from multiprocessing.spawn import import_main_path
from de.file_utils import *
from files.os.modules.parse_sc import *
import pygame

shortcuts = []

f = child_files(files_root() + '/os/taskbar_shortcuts')
for i in range(len(f)):
    if f[i].endswith('.sc'):
        shortcuts.append(sc_to_dict(files_root() + '/os/taskbar_shortcuts/' + f[i]))
        # shortcuts[i]['icon'] = pygame.image.load(files_root() + shortcuts[i]['icon'][0])
        print(shortcuts[i]['icon'])
        shortcuts[i]['icon'] = pygame.transform.scale(shortcuts[i]['icon'], (1 * 0.8, 1 * 0.8))