import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from PIL import Image
from core.lsystem import main
from core.lsystem import drawer
from core.lsystem import utils


def tree_function(generation: int = 6):
    tree = main.WMLLSystem('FX', 4, {'F': 3, 'X': 0}, {'+': 30, '-': -30},
                           ['F->FF', 'X->F[+XF--FF*+++FX-F*]X'])
    tree.generate(generation)
    return tree


@utils.function_time
def round(tree: main.WMLLSystem):
    win = drawer.ScreenHandler(image_size=(1600, 900))
    pen = drawer.Drawer(win)
    drawer.start(win, tree, pen, None, [450, 900])


if __name__ == '__main__':
    round(tree_function())
