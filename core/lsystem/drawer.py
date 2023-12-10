from PIL import Image
from PIL import ImageDraw
from math import sin, cos, radians
from dataclasses import dataclass, field
from main import BaseLSystem, WMLLSystem


def get_new_coords(coordx: float, coordy: float,
                   angle: float, length: float) -> list[float]:
    new_coordx = coordx - sin(radians(angle)) * length
    new_coordy = coordy - cos(radians(angle)) * length
    return [new_coordx, new_coordy]


@dataclass(init=True, frozen=False)
class Drawer:
    image_size: tuple[int, int] = field(init=True, default=(1600, 900))
    filename: str = field(init=True, default='tree.png')
    thickness_reduction: float = field(init=True, default=1)  # from 0 to 1
    lsystems: list[WMLLSystem] = field(init=False, default_factory=list)
    pre_show: bool = True

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
                  lsystem: WMLLSystem | BaseLSystem) -> None:

        image = Image.new('RGB', self.image_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        coords: list[float] = base_coords
        angle: float = 0
        saved_coords: list[list[float]] = []
        saved_angles: list[float] = []

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

        if self.pre_show:
            image.show()

        image.save(self.filename, "PNG")

    def draw_saved_tree(self, base_coords: list[float], ls_idx: int) -> None:
        self.draw_tree(base_coords, self.lsystems[ls_idx])


if __name__ == '__main__':
    tree = WMLLSystem('FX', 60, {'F': 10, 'X': 0},  # noqa: F405
                      {'-': -28.5, '+': 28.5},
                      ['F->F', 'FF->X', 'X->F[+F][F][-F]X'])
    tree.thickness = 4
    tree.generate(4)
    print(tree.state)
    pen = Drawer((1500, 1000), 'treesecond.png')
    pen.append_lsystem(tree)
    pen.draw_saved_tree([350, 1000], 0)
