import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.lsystem import main
from core.lsystem import drawer
from core.lsystem import utils


def serpinskiy(generation: int = 7):
    tree = main.WMLLSystem('F-G-G', 3, {'F': 6, 'G': 6},
                           {'+': 120, '-': -120}, ['F->F-G+F+G-F', 'G->GG'])
    tree.generate(generation)
    return tree

@utils.function_time
def round(tree: main.WMLLSystem):
    win = drawer.ScreenHandler(image_size=(1600, 900))
    pen = drawer.Drawer(win, thickness_reduction=0.5)
    drawer.start(win, tree, pen, None, [450, 900])

if __name__ == '__main__':
    round(serpinskiy())
