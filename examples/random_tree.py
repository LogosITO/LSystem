import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from core import lsystem
from core.lsystem import main
from core.lsystem import drawer
from core.lsystem import generator
from core.lsystem import utils
from core.lsystem import rule
from core.lsystem import drawing_presets

if __name__ == '__main__':
    win = drawer.ScreenHandler((200, 200, 200, 0), (1, 1), (1600, 900), 'PNG')
    pen = drawer.Drawer(win, "random_tree")

    MRG = generator.ManualRuleGenerator()
    MRG.groups_to_delete = ['RRN', 'RLN']
    MRG.alphabet = 'FXY'

    LG = generator.LSystemGenerator()
    LG.angles_values_borders = utils.IPair(-30, 30)
    LG.set_generator(MRG)
    tree = LG.out()

    tree.axiom = ''.join(tree.alphabet.keys())
    tree.add_rule('F->FF')
    tree.generate(5)
    pen.append_lsystem(tree)
    pen.draw_saved_tree([350, 800], 0, drawer.FinalState.Showing)
