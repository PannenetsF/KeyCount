import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import argparse
from keyconst import *
from keycount import load_keys


def norm_keys(key_dict):
    key_sum = sum(key_dict[i] for i in key_dict.keys())
    for i in key_dict.keys():
        key_dict[i] = key_dict[i] * 1.0 / key_sum
    return key_dict


parser = argparse.ArgumentParser("keyvisual")
parser.add_argument('--file',
                    type=str,
                    default='./file.json',
                    help='data file')
parser.add_argument('--colormap',
                    type=str,
                    default='hot_r',
                    help='you can change the style, based on pyplot colormap')
parser.add_argument('--save',
                    type=str,
                    default='./myheat.png',
                    help='file name to save')
parser.add_argument('--dpi',
                    type=int,
                    default=960,
                    help='dpi to save the file')
args = parser.parse_args()

key_dict = load_keys(args)
key_dict = norm_keys(key_dict)

key_mat = np.zeros((key_total_height, key_total_length))
row_idx = 0
cb = iter(colbrk)
back = 0

fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(len(key)):
    rb = iter(rowbrk[i])
    row_idx_next = row_idx + key_height
    col_idx = 0
    for k, ke in enumerate(key[i]):
        col_idx_next = col_idx + key_length[key_map[ke]]
        key_mat[row_idx:row_idx_next,
                col_idx:col_idx_next] = key_dict[str(ke)]  # key
        col_idx = col_idx_next
        if k != len(key[i]) - 1:
            col_idx_next += key_break[next(rb)]
            key_mat[row_idx:row_idx_next, col_idx:col_idx_next] = back  # break
            col_idx = col_idx_next
    row_idx = row_idx_next
    if i != len(key) - 1:
        row_idx_next = row_idx + key_break[next(cb)]
        key_mat[row_idx:row_idx_next, :] = back  # break
        row_idx = row_idx_next

plt.xticks([])
plt.yticks([])
plt.axis('off')
im = ax.imshow(key_mat, cmap=getattr(plt.cm, args.colormap))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
plt.savefig(args.save, dpi=args.dpi)
# plt.show()
print('saved at ' + args.save)
