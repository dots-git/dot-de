#!/usr/bin/env python3
from de.scripts.file_utils import *

# Exported Class
class DotFiles(object):
    def __init__(self, starting_path):
        self.path = starting_path
    
    def visit(self, folder):
        for f in child_dirs(self.path):
            if f == folder:
                self.path += '/' + f
                return 1
        return 0
    
    def go_back(self):
        for i in range(len(self.path)):
            j = len(self.path) - i - 1

            if self.path[j] == '/' or self.path[j] == '\\':
                self.path = self.path[0:j]
                return 1
        return 0
    
    def ls(self):
        return children(self.path)
    
    def ls_dir(self):
        return child_dirs(self.path)
    