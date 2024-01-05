import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core.lsystem import main
from core.lsystem import drawer


def serpinskiy(generation: int = 7):
    tree = main.WMLLSystem('F-G-G', 3, {'F': 6, 'G': 6},
                           {'+': 120, '-': -120}, ['F->F-G+F+G-F', 'G->GG'])
    tree.generate(generation)
    return tree


if __name__ == '__main__':
    win = drawer.ScreenHandler()
    pen = drawer.Drawer(win, 'serpinskiy.png')
    pen.append_lsystem(serpinskiy())
    pen.draw_saved_tree([350, 850], 0)
