import numpy as np

from matplotlib import cm
from enum import Enum, unique


__all__ = ['Color', 'Colormap']

# reference: https://www.matplotlib.org.cn/tutorials/colors/colormaps.html#miscellaneous
_paired_colors = [[int(v * 255) for v in color][::-1] for color in cm.get_cmap('Paired').colors]


@unique
class Color(Enum):
    none = [-1, -1, -1]
    Black = [0, 0, 0]
    White = [255, 255, 255]
    blue = _paired_colors[0]
    Blue = _paired_colors[1]
    green = _paired_colors[2]
    Green = _paired_colors[3]
    red = _paired_colors[4]
    Red = _paired_colors[5]
    yellow = _paired_colors[6]
    Yellow = _paired_colors[7]
    purple = _paired_colors[8]
    Purple = _paired_colors[9]
    brown = _paired_colors[10]
    Brown = _paired_colors[11]



def voc_palette(N=256):
    def bit_get(val, idx):
        return (val & (1 << idx)) != 0

    ret = np.zeros((N, 3), dtype=np.uint8)
    for i in range(N):
        r = g = b = 0
        c = i
        for j in range(8):
            r |= (bit_get(c, 0) << 7 - j)
            g |= (bit_get(c, 1) << 7 - j)
            b |= (bit_get(c, 2) << 7 - j)
            c >>= 3
        ret[i, :] = [r, g, b]
    return ret.tolist()


Colormap = voc_palette()
