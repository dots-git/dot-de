import numpy as np

def print_dict(in_dict: dict, depth: int = 0) -> None:
    for key in in_dict.keys():
        for i in range(depth):
            print(' │ ', end='')
        if isinstance(in_dict[key], dict):
            print(str(key))
            print_dict(in_dict[key], depth + 1)
        else:
            print(str(key) + ': ' + str(in_dict[key]))
    

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)