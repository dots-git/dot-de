import numpy as np

# def approx_offset(a: np.ndarray):
#     n = 4
#     offset_array = np.zeros(a.shape)
#     zeros = np.zeros((n))
#     coefficients = np.zeros((n))
#     for i in range(n):
#         zeros[i] = np.sqrt(1 / (10**(-0.5*i)))
#         coefficients[i] = 0.5 * a * zeros[i]
#     for i in range(n):
#         offset_array += 

def offset(shape, d) -> np.ndarray:
    b = -1/(d**3)
    a = np.zeros(shape)
    x = np.mgrid[0:d, 0:shape[1]][0]
    a[:d] += b * np.power((x - d), 3)
    return a
    

print(offset((5, 3), 4).transpose())
