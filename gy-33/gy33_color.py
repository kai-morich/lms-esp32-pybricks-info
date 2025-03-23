from pybricks.parameters import Color

# from https://github.com/python/cpython/blob/main/Lib/colorsys.py
def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    rangec = (maxc-minc)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = rangec / maxc
    rc = (maxc-r) / rangec
    gc = (maxc-g) / rangec
    bc = (maxc-b) / rangec
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v

def rgbc_to_hsv(r, g, b, c):
    h, s, v = rgb_to_hsv(r, g, b)
    return h, s, c

def rgbc_to_hsv_Color(r, g, b, c, c_max=3200) -> Color:
    h, s, v = rgb_to_hsv(r, g, b)
    return Color(h*360, s*100, c*100/c_max)

def hsv_to_standard_Color(col: Color) -> Color:
    """get nearest standard color. adapt to needed colors per use case"""
    if col.s < 40:
        if col.v < 50:                  return Color.NONE
        else:                           return Color.WHITE
    else:
        if col.h > 300 or col.h < 30:   return Color.RED
        elif col.h < 75:                return Color.YELLOW
        elif col.h < 195:               return Color.GREEN
        else:                           return Color.BLUE
