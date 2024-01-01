from PIL import Image
from PIL import ImageDraw
from math import sin, cos, radians
from dataclasses import dataclass, field
from main import BaseLSystem, WMLLSystem
from utils import get_memory_usage, function_time
from enum import Enum


def get_new_coords(coordx: float, coordy: float,
                   angle: float, length: float) -> list[float]:
    new_coordx = coordx - sin(radians(angle)) * length
    new_coordy = coordy - cos(radians(angle)) * length
    return [new_coordx, new_coordy]


class FinalState(Enum):
    Nothing = 0
    Saving = 1
    Showing = 2
    Default = 3


@dataclass(init=True, frozen=False)
class ScreenHandler:
    bg_color: tuple[int] = field(init=True, default=(255, 255, 255, 0))
    image_size: tuple[int, int] = field(init=True, default=(1600, 900))
    img: ImageDraw = field(init=False)
    pen: ImageDraw.Draw = field(init=False)

    def create_screen(self) -> ImageDraw.Draw:
        self.img = Image.new('RGB', self.image_size, self.bg_color)
        self.pen = ImageDraw.Draw(self.img)
        return self.pen

    def end_work(self, filename: str, show_state: bool = True):
        if show_state:
            self.img.show()
        self.img.save(filename, "PNG")

    def show(self):
        self.img.show()


@dataclass(init=True, frozen=False)
class Drawer:
    screen: ScreenHandler = field(init=True, default_factory=ScreenHandler)
    filename: str = field(init=True, default="tree")
    thickness_reduction: float = field(init=True, default=1)  # from 0 to 1
    lsystems: list[WMLLSystem] = field(init=False, default_factory=list)
    pre_show: bool = True

    def __post_init__(self):
        self.screen.create_screen()

    def append_lsystem(self, lsystem: WMLLSystem | BaseLSystem) -> None:
        self.lsystems.append(lsystem)

    def extend_lsystems(self, lsystems: list[WMLLSystem]) -> None:
        self.lsystems.extend(lsystems)

    def draw_leaf(self, img_pen: ImageDraw.Draw, coords: list[float]):
        img_pen.ellipse((coords[0], coords[1], coords[0] + 15,
                        coords[1] + 20), fill='green', outline=(0, 0, 0))

    def draw_step(self, img_pen: ImageDraw.Draw, step: str, crd: list[float],
                  angle: float, ls: WMLLSystem | BaseLSystem) -> list[float]:
        newcoords = get_new_coords(crd[0], crd[1],
                                   angle, ls.alphabet[step])
        img_pen.line((crd[0], crd[1], newcoords[0], newcoords[1]),
                     width=ls.thickness, fill='black')
        return newcoords

    def draw_tree(self, base_coords: list[float],
                  lsystem: WMLLSystem | BaseLSystem,
                  with_end: FinalState = FinalState.Default) -> None:
        draw = self.screen.pen
        coords, angle = base_coords, 0
        saved_coords, saved_angles = [], []

        for step in lsystem.state:
            lsystem.thickness = (self.thickness_reduction * lsystem.thickness)
            if step == '[':
                saved_coords.append(coords)
                saved_angles.append(angle)
            elif step == ']':
                try:
                    coords = saved_coords.pop()
                    angle = saved_angles.pop()
                except IndexError:
                    pass
            try:
                if step == lsystem.leaf_symbol:
                    self.draw_leaf(draw, coords)
            except AttributeError:
                pass
            if step in lsystem.alphabet:
                coords = self.draw_step(draw, step, coords, angle, lsystem)
            elif step in lsystem.angles:
                angle += lsystem.angles[step]

        self.final_catcher(self.filename, with_end)

    def final_catcher(self, filename: str, with_end: FinalState):
        match with_end:
            case FinalState.Saving:
                self.screen.end_work(self.filename, False)
            case FinalState.Showing:
                self.screen.show()
            case FinalState.Default:
                self.screen.end_work(self.filename, True)

    def draw_saved_tree(self, base_coords: list[float], ls_idx: int,
                        with_end: FinalState = FinalState.Default) -> None:
        self.draw_tree(base_coords, self.lsystems[ls_idx])

    def draw_saved_trees(self, base_coords: list[list[float]],
                         with_end: FinalState = FinalState.Saving) -> None:
        if len(self.lsystems) == len(base_coords):
            for idx, ls in enumerate(self.lsystems):
                self.draw_tree(base_coords[idx], ls, FinalState.Nothing)
            else:
                self.final_catcher(self.filename, with_end)
        else:
            raise IndexError("Can't math base_coords with lsystems")


@function_time
def main():
    win = ScreenHandler()
    tree = WMLLSystem('XFX', 60, {'F': 10, 'G': 4, 'X': 0, 'Y': 12},  # noqa: F405
                      {'-': -28.5, '+': 28.5, '#': -10, '@': 10},
                      ['X[0.5]->XX[#YX@]GG', 'F->JFF'])
    tree.thickness = 4
    tree.generate(6)
    pen = Drawer(win, 'tree.png')
    pen.append_lsystem(tree)
    pen.draw_saved_tree([350, 900], 0)
    print(get_memory_usage())


if __name__ == '__main__':
    main()
