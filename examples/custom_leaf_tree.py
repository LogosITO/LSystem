import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from PIL import Image
from core import lsystem
from core.lsystem import main
from core.lsystem import drawer
from core.lsystem import utils


leaf_img = None


def leaf_function(*args):
    coords = tuple(map(int, args[2]))
    global leaf_img
    if not leaf_img:
        leaf_img = Image.open(r'LSystem\assets\images\example-bow.png').convert('RGBA')
    leaf_img = leaf_img.resize((15, 15))
    args[0].paste(leaf_img, coords, leaf_img)


def tree_function(generation: int=6):
    tree = main.WMLLSystem('FX', 4, {'F': 3, 'X': 0}, {'+': 30, '-': -30},
                           ['F->FF', 'X->F[+XF--FF*+++FX-F*]X'])
    tree.generate(generation)
    return tree

@utils.function_time
def round(tree: main.WMLLSystem, leaf: callable):
    win = drawer.ScreenHandler()
    pen = drawer.Drawer(win, leaf_drawing_function=leaf)

    pen.append_lsystem(tree)
    pen.draw_saved_tree([550, 800], 0, drawer.FinalState.Showing)

if __name__ == '__main__':
    round(tree_function(), leaf_function)