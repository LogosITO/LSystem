from PIL import Image
from PIL import ImageDraw, ImageOps
from math import sin, cos, radians
from dataclasses import dataclass, field
from main import BaseLSystem, WMLLSystem, StateHandler
from utils import get_memory_usage, function_time
import drawing_presets as dp
from enum import Enum
from typing import Final, Optional
from threading import Thread


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


image_formats: Final[list[str]] = ['BMP', 'PNG', 'JPEG', 'TGA']


@dataclass(init=True, frozen=False)
class ScreenHandler:
    bg_color: tuple[int] = field(init=True, default=(255, 255, 255))
    transparency: tuple[int] = field(init=True, default=(220, 220))
    image_size: tuple[int] = field(init=True, default=(1600, 900))
    image_format: str = field(init=True, default='PNG')
    img: Image = field(init=False)
    bg_img: Image = field(init=False, default=None)
    pen: ImageDraw.Draw = field(init=False)

    def __post_init__(self):
        try:
            idx = image_formats.index(self.image_format.upper())
            self.format = image_formats[idx]
        except:
            self.format = 'PNG'

    def set_bg_image(self, path_string: str) -> bool:
        self.bg_img = Image.open(path_string).convert('RGBA')
        self.bg_img = self.bg_img.resize(self.image_size)

    def create_screen(self) -> ImageDraw.Draw:
        self.img = Image.new('RGBA', self.image_size, self.bg_color)
        if self.bg_img is not None:
            self.img.paste(self.bg_img, None, self.bg_img)
        self.pen = ImageDraw.Draw(self.img)
        return self.pen

    def end_work(self, filename: str, show_state: bool = True) -> None:
        if show_state:
            self.img.show()
        self.img.save(filename+'.'+self.image_format.lower())

    def show(self) -> None:
        self.img.show()


@dataclass(init=True, frozen=False)
class Drawer:
    screen: ScreenHandler = field(init=True, default_factory=ScreenHandler)
    filename: str = field(init=True, default="tree")
    thickness_reduction: float = field(init=True, default=1)  # from 0 to 1
    fg_color: tuple[int] = field(init=True, default=(101, 67, 33))
    leaf_name: Optional[str] = field(init=True, default='example-leaf.png')
    lsystems: list[WMLLSystem] = field(init=False, default_factory=list)
    pre_show: bool = True

    def __post_init__(self):
        self.screen.create_screen()

    def append_lsystem(self, lsystem: WMLLSystem | BaseLSystem) -> None:
        self.lsystems.append(lsystem)

    def extend_lsystems(self, lsystems: list[WMLLSystem]) -> None:
        self.lsystems.extend(lsystems)

    def draw_leaf(self, img: Image, img_pen: ImageDraw.Draw,
                  coords: list[float], screen_size: tuple[int]) -> None:
        if self.leaf_name is not None:
            dp.draw_uploaded_leaf(img, img_pen, coords, screen_size, name=self.leaf_name)
        else:
            dp.draw_ellipse_leaf(img, img_pen, coords, screen_size)

    def draw_step(self, img_pen: ImageDraw.Draw, step: str, crd: list[float],
                  angle: float, ls: WMLLSystem | BaseLSystem, th_ml: float = 1) -> list[float]:
        newcoords = get_new_coords(crd[0], crd[1], angle, ls.alphabet[step])
        img_pen.line((crd[0], crd[1], newcoords[0], newcoords[1]),
                     width=int(ls.thickness * th_ml), fill=self.fg_color)
        return newcoords

    def draw_tree(self, base_coords: list[float],
                  lsystem: WMLLSystem | BaseLSystem,
                  with_end: FinalState = FinalState.Default) -> None:
        lsystem.state = StateHandler(lsystem.state).out()
        image = self.screen.img
        draw = self.screen.pen
        coords, angle = base_coords, 0
        saved_coords, saved_angles = [], []

        for idx, step in enumerate(lsystem.state):
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
                    self.draw_leaf(image, draw, coords, self.screen.image_size)
            except AttributeError:
                pass
            if step in lsystem.alphabet:
                try:
                    next_step = lsystem.state[idx + 1]
                except IndexError:
                    next_step = 'end'
                th_ml = 1
                if next_step == '|':
                    th_ml = 1.65
                coords = self.draw_step(draw, step, coords, angle, lsystem, th_ml)
            elif step in lsystem.angles:
                angle += lsystem.angles[step]

        self.final_catcher(self.filename, with_end)

    def final_catcher(self, filename: str, with_end: FinalState) -> None:
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


def start(win: ScreenHandler, tree: WMLLSystem, pen: Drawer, bg_fn: Optional[str], coords: list[int, int]):
    t1 = Thread(target=tree.generate, args=(6, ))
    if bg_fn:
        win.set_bg_image(bg_fn)
    pen.thickness_reduction = 0.9997
    pen.append_lsystem(tree)
    t2 = Thread(target=pen.draw_saved_tree, args=(coords, 0, ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def mirroring(fn: str, img_path: str, cdr: list[int, int]):
    start_img = Image.open(img_path).convert('RGBA')
    new_img = ImageOps.mirror(start_img)
    start_img.paste(new_img, cdr)
    start_img.save(fn.endswith('.') + 'mirrored' + '.png')
    start_img.show()

@function_time
def main():
    tree = WMLLSystem('XFX', 4, {'F': 10, 'G': 4, 'X': 0, 'Y': 12},  # noqa: F405
                      {'-': -28.5, '+': 28.5, '#': -10, '@': 10},
                      ['X->F[+FX*-XFF*+GF*]F', 'F->GF'])
    win = ScreenHandler(transparency=(1, 1))
    pen = Drawer(win, 'tree', leaf_name='example-leaf')
    start(win, tree, pen, r'LSystem\assets\images\background-field.png', [450, 600])
    mirroring('tree', r'C:\Users\Asus\Desktop\LSystem', [450, 600])
    print(get_memory_usage())


if __name__ == '__main__':
    main()
