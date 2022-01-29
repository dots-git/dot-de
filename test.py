
import os

def child_dirs(d):
    return [name for name in os.listdir(d)
            if os.path.isdir(os.path.join(d, name))]

def child_files(d):
    return [name for name in os.listdir(d)
            if not os.path.isdir(os.path.join(d, name))]

def children(d):
    return [name for name in os.listdir(d)]

p = os.path.dirname(os.path.realpath(__file__))

print(children(p))