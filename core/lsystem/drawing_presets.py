from PIL import Image
from os import listdir
from os.path import isfile, join
from difflib import SequenceMatcher
from typing import Final


MATCH_CONSTANT: Final[float] = 0.65
leafs = {}
backgrounds = {}


def auto_upload_all_resources(mypath=r'LSystem\assets\images'):
    global leafs, backgrounds
    if len(leafs) != 0 and len(backgrounds) != 0:
        return
    filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for filename in filenames:
        path = mypath + '\\' +  filename
        img = Image.open(path).convert('RGBA')
        if 'leaf' in filename or 'lf' in filename or 'лист' in filename:
            leafs.update({filename: img})
        else:
            backgrounds.update({filename: img})


def find_most_similar_name(req, dct):
    idx, MMC = None, 0 
    for name in dct.keys():
        MC = SequenceMatcher(None, name, req).ratio()
        if MC > MATCH_CONSTANT or req in name:
            MMC = max(MMC, MC)
            idx = name
    return idx


upl_name = None


def draw_uploaded_leaf(*args, name):
    global upl_name, leafs
    if upl_name is None:
        leaf_idx = find_most_similar_name(name, leafs)
        upl_name = leaf_idx
    else:
        leaf_idx = upl_name
    screen = args[3]
    xsize, ysize = int(screen[0] * 0.015), int(screen[1] * 0.022)
    coords = tuple(map(int, args[2]))
    leaf_img = leafs[leaf_idx]
    leaf_img = leaf_img.resize((xsize, ysize))
    args[0].paste(leaf_img, coords, leaf_img)


def draw_ellipse_leaf(*args):
    screen = args[3]
    xsize, ysize = int(screen[0] * 0.015), int(screen[1] * 0.022)
    coords = args[2]
    args[1].ellipse((coords[0], coords[1], coords[0] + xsize,
                    coords[1] + ysize), fill='green', outline=(0, 0, 0))

auto_upload_all_resources()