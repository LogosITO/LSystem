from PIL import Image


leaf_img = None


def draw_ellipse_leaf(*args):
    screen = args[3]
    xsize, ysize = int(screen[0] * 0.015), int(screen[1] * 0.022)
    coords = args[2]
    args[1].ellipse((coords[0], coords[1], coords[0] + xsize,
                    coords[1] + ysize), fill='green', outline=(0, 0, 0))


def draw_real_leaf(*args):
    screen = args[3]
    xsize, ysize = int(screen[0] * 0.015), int(screen[1] * 0.022)
    coords = tuple(map(int, args[2]))
    global leaf_img
    if not leaf_img:
        leaf_img = Image.open(r'LSystem\assets\images\example-leaf.png').convert('RGBA')
    leaf_img = leaf_img.resize((xsize, ysize))
    args[0].paste(leaf_img, coords, leaf_img)


def draw_canadian_leaf(*args):
    screen = args[3]
    xsize, ysize = int(screen[0] * 0.015), int(screen[1] * 0.022)
    coords = tuple(map(int, args[2]))
    global leaf_img
    if not leaf_img:
        leaf_img = Image.open(r'LSystem\assets\images\example-canadian-leaf.png').convert('RGBA')
    leaf_img = leaf_img.resize((xsize, ysize))
    args[0].paste(leaf_img, coords, leaf_img)
