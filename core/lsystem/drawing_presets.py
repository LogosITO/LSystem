from PIL import Image


leaf_img = None


def draw_ellipse_leaf(*args):
    coords = args[2]
    args[1].ellipse((coords[0], coords[1], coords[0] + 15,
                    coords[1] + 20), fill='green', outline=(0, 0, 0))


def draw_real_leaf(*args):
    coords = tuple(map(int, args[2]))
    global leaf_img
    if not leaf_img:
        leaf_img = Image.open(r'LSystem\assets\images\example-leaf.png').convert('RGBA')
    leaf_img = leaf_img.resize((15, 15))
    args[0].paste(leaf_img, coords, leaf_img)


def draw_canadian_leaf(*args):
    coords = tuple(map(int, args[2]))
    global leaf_img
    if not leaf_img:
        leaf_img = Image.open(r'LSystem\assets\images\example-canadian-leaf.png').convert('RGBA')
    leaf_img = leaf_img.resize((15, 15))
    args[0].paste(leaf_img, coords, leaf_img)
