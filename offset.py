import numpy as np

def offset(shape, d) -> np.ndarray:
    b = -1/(d**3)
    a = np.zeros(shape)
    x = np.mgrid[0:d, 0:shape[1]][0]
    a[:d] += b * np.power((x - d), 3)
    return a
    

print(offset((5, 3), 4).transpose())
