import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.lsystem import main
from core.lsystem import drawer


def tree1(generation: int = 5):
    tree = main.WMLLSystem('FX', 10, {'X': 0, 'F': 8}, {'+': 30, '-': 30},
                           ['X>F->F[+XFXF-X*]', 'F<X->F[-XFXF+X*]', 'F->FF'])
    tree.generate(generation)
    return tree


def tree2(generation: int = 5):
    tree = main.WMLLSystem('X', 6, {'X': 0, 'F': 8}, {'+': 28.5, '-': 28.5},
                           ['X->F-[[X]+X*]+F[+FX]-X*', 'F->FF'])
    tree.generate(generation)
    return tree


def tree3(generation: int = 5):
    tree = main.WMLLSystem('XF', 6, {'X': 0, 'F': 8}, {'+': 28.5, '-': 28.5},
                           ['X->F*F[X-F*X+F*F*-[X-F*FX+F*]]'])
    tree.generate(generation)
    return tree


if __name__ == '__main__':
    win = drawer.ScreenHandler((250, 100, 100, 10), (1920, 1080))
    pen = drawer.Drawer(win, 'several_trees.png')
    pen.extend_lsystems([tree1(), tree2(), tree3()])
    pen.draw_saved_trees([[530, 850], [1060, 850], [1590, 850]], drawer.FinalState.Showing)
