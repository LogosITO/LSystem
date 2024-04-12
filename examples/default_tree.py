import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.lsystem import main
from core.lsystem import drawer
from core.lsystem import utils


def small_tree():
    tree = main.WMLLSystem('XF', 6, {'F': 10, 'J': 4, 'X': 0},
                           {'-': -28.5, '+': 28.5, '#': -5, '^': 10},
                           ['X->XF[+FX-F*]#[XF+F-J*]', 'F->JFF'])
    tree.generate(4)
    return tree

@utils.function_time
def round(tree: main.WMLLSystem):
    win = drawer.ScreenHandler(image_size=(1600, 900))
    pen = drawer.Drawer(win)
    drawer.start(win, tree, pen, None, [450, 900])

if __name__ == '__main__':
    round(small_tree())
