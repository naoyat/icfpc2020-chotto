#!/usr/bin/env python
import sys
import os
import numpy as np
import click

from dataio.png import read_from_png, write_to_png
from dataio.wav import read_from_wav, write_to_wav
from dataio.text import read_from_text, write_to_text
from parser import *


def pp_data(d, one='#', zero=' ', remove_frame=False):
    def pp(r, c0, c1):
        buf = []
        for c in range(c0, c1):
            buf.append(one if d[r, c] > 0 else zero)
        return ''.join(buf)

    H, W = d.shape
    for r in range(H):
        if remove_frame:
            if r == 0 or r == H - 1:
                continue
            row = pp(r, 1, W-1)
        else:
            row = pp(r, 0, W)
        print(row)



@click.command()
@click.argument('path', type=click.Path())
@click.option('--view', is_flag=True, default=False)
def main(path, view):
    if path.endswith('.wav'):
        d = read_from_wav(path)
    elif path.endswith('.png'):
        d = read_from_png(path)
    else:
        d = None

    # print(d)
    # if view:
    #     write_to_png(d, 'tmp.png', True)

    pp_data(d)
    p = parse_data(d)
    print(p)


if __name__ == '__main__':
    main()
