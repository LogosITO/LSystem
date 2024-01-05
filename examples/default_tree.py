import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core import lsystem
from core.lsystem import main
from core.lsystem import drawer

def small_tree():
    tree = main.WMLLSystem('XF', 7, {'F': 10, 'J': 4, 'X': 0},  
                                {'-': -28.5, '+': 28.5, '#': -5, '^': 10},
                                ['X->XF[+FX-F*]#[XF+F-J*]', 'F->JFF'])
    tree.generate(5)
    print(tree.state)
    return tree

if __name__ == '__main__':
    win = drawer.ScreenHandler()
    pen = drawer.Drawer(win, 'default_tree.png', 1)
    pen.thickness_reduction = 0.9996
    pen.append_lsystem(small_tree())
    pen.draw_saved_trees([[350, 850]], drawer.FinalState.Default)