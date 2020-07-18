import os
import numpy as np
from imageio import imread, imwrite


def read_from_png(png_file): # png -> darray
    im = imread(png_file)
    # print(im.shape, im.dtype)
    # [H * W * 4:[r,g,b,a]]
    H, W, _ = im.shape
    H >>= 2
    W >>= 2
    # print('H=%d W=%d' % (H,W))
    d = np.zeros((H, W), dtype=int)
    for r in range(H):
        for c in range(W):
            d[r,c] = im[4*r+2, 4*c+2, 0] >= 128
    return d


def write_to_png(d, png_file, cell_size=4, show=False):
    H, W = d.shape
    im = np.zeros((cell_size*H, cell_size*W, 4), dtype='uint8')
    for r in range(H):
        for c in range(W):
            im[cell_size*r:cell_size*(r+1), cell_size*c:cell_size*(c+1), 0:3] = 192 * d[r,c]
            im[cell_size*r:cell_size*(r+1)-1, cell_size*c:cell_size*(c+1)-1, 0:3] = 255 * d[r,c]

            # im[4*r:4*(r+1), 4*c:4*(c+1), 0:3] = 255 * d[r,c]
            im[cell_size*r:cell_size*(r+1), cell_size*c:cell_size*(c+1), 3] = 255
    imwrite(png_file, im)
    if show:
        os.system('open '+png_file)


if __name__ == '__main__':
    # main()
    d = read_from_png('img/message2.png')
    print(d)
    write_to_png(d, 'foo.png', show=True)
