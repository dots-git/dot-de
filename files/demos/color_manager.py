def rgb_to_hsv(r, g = -1, b = -1):
    if g == -1:
        g = r[1]
        b = r[2]
        r = r[0]
    r /= 255
    g /= 255
    b /= 255

    c_max = max(r, g, b)
    c_min = min(r, g, b)

    delta = c_max - c_min
    
    h = 0.
    if c_max == c_min:
        h = 0.
    elif c_max == r:
        h = 1 / 6 * ((g - b)/delta % 6)
    elif c_max == g:
        h = 1 / 6 * ((b - r)/delta + 2)
    elif c_max == b:
        h = 1 / 6 * ((r - g)/delta + 4)
    
    s = 0.
    if c_max != 0:
        s = delta/c_max
    
    v = c_max

    return h, s, v

def hsv_to_rgb(h, s = -1, v = -1):
    if s == -1:
        s = h[1]
        v = h[2]
        h = h[0]

    deg_60 = 1 / 6

    c = v * s
    x = c * (1 - abs((h / deg_60) % 2 - 1))
    m = v - c

    r, g, b = (0, 0, 0)

    if h < deg_60:
        r, g, b = c, x, 0
    elif deg_60 <= h < 2*deg_60:
        r, g, b = x, c, 0
    elif 2*deg_60 <= h < 3*deg_60:
        r, g, b = 0, c, x
    elif 3*deg_60 <= h < 4*deg_60:
        r, g, b = 0, x, c
    elif 4*deg_60 <= h < 5*deg_60:
        r, g, b = x, 0, c
    elif 5*deg_60 <= h < 6*deg_60:
        r, g, b = c, 0, x

    r, g, b = r+m, g+m, b+m
    return round(r * 255), round(g * 255), round(b * 255)

def hsv(a, b = -1, c = -1, source_space = 'rgb'):
    if source_space == 'rgb':
        return rgb_to_hsv(a, b, c)

def rgb(a, b = -1, c = -1, source_space = 'hsv'):
    if source_space == 'hsv':
        return hsv_to_rgb(a, b, c)

h = 0/360
s = 1
v = 1
print(hsv(0, 255, 0))
print(rgb((h, s, v)))