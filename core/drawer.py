from PIL import Image
from PIL import ImageDraw
from math import sin, cos, radians
from dataclasses import dataclass
from lsystem import *   # type: ignore # noqa: F403


def get_new_coords(coordx: float, coordy: float,
                   angle: float, length: float) -> list[float]:
    new_coordx = coordx - sin(radians(angle)) * length
    new_coordy = coordy - cos(radians(angle)) * length
    return [new_coordx, new_coordy]


@dataclass(init=True, frozen=True)
class Drawer:
    image_size: tuple[int, int] = field(init=True, default=(1920, 1080))
    filename: str = field(init=True, default='tree.png')
    lsystems: list[BaseLSystem] = field(init=False, default_factory=list)

    def append_lsystem(self, lsystem: BaseLSystem):
        self.lsystems.append(lsystem)
    
    def extend_lsystem(self, lsystems: list[BaseLSystem]):
        self.lsystems.extend(lsystems)

    def draw_tree(self, base_coords: list[int], lsystem: WMLLSystem):

        image = Image.new('RGB', self.image_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        coords: list[float] = base_coords
        angle: float = 0
        saved_coords: list[list[float]] = []
        saved_angles: list[float] = []

        for move in lsystem.state:
            if move == '[':
                saved_coords.append(coords)
                saved_angles.append(angle)
            elif move == ']':
                coords = saved_coords.pop()
                angle = saved_angles.pop()
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

        image.save(self.filename, "PNG")
    
    def draw_tree_from_saved(self, base_coords: list[int], ls_idx: int):
        self.draw_tree(base_coords, self.lsystems[ls_idx])

    


if __name__ == '__main__':
    tree = WMLLSystem('X', 1, {'F': 15, 'X': 0},  # noqa: F405
                      {'-': -30.5, '+': 30.5},
                      ['X[0.9]->F-[[X]+X*]+F[+FX]-X*', 'F->FF'])
    tree.generate(5)
    pen = Drawer((2000, 2000), 'treelol.png')
    pen.append_lsystem(tree)
    pen.draw_tree_from_saved([1000, 1000], 0)