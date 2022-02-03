import os as pyos

def child_dirs(d):
    return [name for name in pyos.listdir(d)
            if pyos.path.isdir(pyos.path.join(d, name))]

def child_files(d):
    return [name for name in pyos.listdir(d)
            if not pyos.path.isdir(pyos.path.join(d, name))]

def children(d):
    return [name for name in pyos.listdir(d)]

def back(d: str) -> str:
    return pyos.path.normpath(d + pyos.sep + pyos.pardir)

def working_dir():
    return pyos.path.dirname(pyos.path.realpath(__file__))

def files_root():
    return back(working_dir()) + pyos.sep + 'files'

def local_file_location(f: str) -> str:
    return back(f).replace(files_root(), '')