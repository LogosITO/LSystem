import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core import lsystem
from core.lsystem import main
from core.lsystem import drawer
from core.lsystem import generator

if __name__ == '__main__':
    win = drawer.ScreenHandler()
    pen = drawer.Drawer()
    tree: main.WMLLSystem = generator.LSystemGenerator().out()
    print(tree.rules)
    tree.generate(5)
    pen.append_lsystem(tree)
    pen.draw_saved_tree([350, 900], 0, drawer.FinalState.Showing)
