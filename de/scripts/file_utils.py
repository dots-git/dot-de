import os

def child_dirs(d):
    return [name for name in os.listdir(d)
            if os.path.isdir(os.path.join(d, name))]

def child_files(d):
    return [name for name in os.listdir(d)
            if not os.path.isdir(os.path.join(d, name))]

def children(d):
    return [name for name in os.listdir(d)]

def back(d):
    return os.path.normpath(d + os.sep + os.pardir)

def working_dir():
    return os.path.dirname(os.path.realpath(__file__))

def script_root():
        return back(working_dir())

def files_root():
    return back(back(working_dir())) + '/files'