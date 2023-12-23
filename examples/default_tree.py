import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core import lsystem
from core.lsystem import main
from core.lsystem import drawer

def small_tree():
    tree = main.WMLLSystem('XF', 5, {'F': 10, 'J': 4, 'X': 0},  
                                {'-': -28.5, '+': 28.5, '#': -5, '^': 10},
                                ['X->XF[+FX-F*]#[XF+F-J*]', 'F->JFF'])
    tree.generate(4)
    return tree

if __name__ == '__main__':
    win = drawer.ScreenHandler()
    pen = drawer.Drawer(win, 'tree.png', 1)
    pen.append_lsystem(small_tree())
    pen.append_lsystem(small_tree())
    pen.draw_saved_tree([350, 850], 0)
    pen.draw_saved_trees([[350, 850], [700, 900]])