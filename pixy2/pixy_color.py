from pybricks.parameters import Color

def rgb_to_hsv(r, g, b):
    """
    copied from python stdlib colorsys.py, adapted to pixy & pybricks ranges:
      in:  r,g,b (0-255)
      out: h (0-359), s (0-100), v (0-100)
    """
    maxc = max(r, g, b)
    minc = min(r, g, b)
    rangec = (maxc-minc)
    v = maxc
    if minc == maxc:
        return 0, 0, int(v/2.55)
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
    return int(h*360), int(s*100), int(v/2.55)

def hsv_to_color(h, s, v):
    if s < 50:
        if   v > 60: return Color.WHITE
        elif v > 30: return Color.GRAY
        else:        return Color.BLACK
    else:
        if h > 300 or h < 30: return Color.RED
        elif h < 75:          return Color.YELLOW
        elif h < 190:         return Color.GREEN
        else:                 return Color.BLUE        
