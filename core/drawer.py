from PIL import Image
from PIL import ImageDraw
from math import sin, cos, radians, floor
from dataclasses import dataclass, field
from lsystem import WMLLSystem


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

    def append_lsystem(self, lsystem: WMLLSystem):
        self.lsystems.append(lsystem)

    def extend_lsystems(self, lsystems: list[WMLLSystem]):
        self.lsystems.extend(lsystems)

    def draw_tree(self, base_coords: list[float], lsystem: WMLLSystem):

        image = Image.new('RGB', self.image_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        coords: list[float] = base_coords
        angle: float = 0
        saved_coords: list[list[float]] = []
        saved_angles: list[float] = []

        for move in lsystem.state:
            lsystem.thickness *= self.thickness_reduction
            lsystem.thickness = floor(lsystem.thickness)
            if move == '[':
                saved_coords.append(coords)
                saved_angles.append(angle)
            elif move == ']':
                try:
                    coords = saved_coords.pop()
                    angle = saved_angles.pop()
                except IndexError:
                    pass
            if move == lsystem.leaf_symbol:
                draw.ellipse((coords[0], coords[1], coords[0] + 15,
                              coords[1] + 20), fill='green', outline=(0, 0, 0))
            if move in lsystem.alphabet:
                newcoords = get_new_coords(coords[0], coords[1],
                                           angle, lsystem.alphabet[move])
                draw.line((coords[0], coords[1], newcoords[0], newcoords[1]),
                          width=lsystem.thickness, fill='black')
                coords = newcoords
            elif move in lsystem.angles:
                angle += lsystem.angles[move]

        if self.pre_show:
            image.show()

        image.save(self.filename, "PNG")

    def draw_tree_from_saved(self, base_coords: list[float], ls_idx: int):
        self.draw_tree(base_coords, self.lsystems[ls_idx])


if __name__ == '__main__':
    tree = WMLLSystem('FX', 60, {'F': 15, 'X': 0},  # noqa: F405
                      {'-': -12.5, '+': 25.5},
                      ['X>F->F[+XFXF-X]', 'F<X->F[-XFXF+X]', 'F->FF'])
    tree.thickness = 4
    tree.generate(4)
    print(tree.state)
    pen = Drawer((1500, 1000), 'treesecond.png')
    pen.append_lsystem(tree)
    pen.draw_tree_from_saved([750, 1000], 0)
