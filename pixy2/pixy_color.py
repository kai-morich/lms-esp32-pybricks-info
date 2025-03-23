from pybricks.parameters import Color

# copied from python stdlib colorsys.py
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

def hsv_to_color(h, s, v):
    if s < 0.5:
        if v > 50: return Color.WHITE
        else:      return Color.BLACK
    else:
        h *= 360
        if h > 300 or h < 30: return Color.RED
        elif h < 75:          return Color.YELLOW
        elif h < 190:         return Color.GREEN
        else:                 return Color.BLUE        
