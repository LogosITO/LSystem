import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core import lsystem
from core.lsystem import main
from core.lsystem import drawer
from core.lsystem import generator
from core.lsystem import utils

if __name__ == '__main__':
    win = drawer.ScreenHandler((200, 200, 200, 50), (1600, 900))
    pen = drawer.Drawer(win, "random_tree")

    MRG = generator.ManualRuleGenerator()
    MRG.expand_deps_dict({'RRN': utils.IPair(1, 1), 'RLN': utils.IPair(2, 2)})
    MRG.alphabet = 'FXY'

    LG = generator.LSystemGenerator()
    LG.set_generator(MRG)
    tree = LG.out()

    tree.generate(5)
    pen.append_lsystem(tree)
    pen.draw_saved_tree([350, 900], 0, drawer.FinalState.Showing)
