import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core import lsystem
from core.lsystem import main
from core.lsystem import drawer

def serpinskiy(generation: int = 6):
    tree = main.WMLLSystem('F-G-G', 4, {'F': 10, 'G': 10}, 
                           {'+': 120, '-': -120}, ['F->F-G+F+G-F', 'G->GG'])
    tree.generate(generation)
    return tree

if __name__ == '__main__':
    win = drawer.ScreenHandler()
    pen = drawer.Drawer(win, 'tree.png')
    pen.append_lsystem(serpinskiy())
    pen.draw_saved_tree([350, 850], 0)