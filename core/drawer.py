from PIL import Image
from PIL import ImageDraw
from math import sin, cos, radians
from lsystem import *   # type: ignore # noqa: F403


def get_new_coords(coordx: float, coordy: float,
                   angle: float, length: float) -> list[float]:
    new_coordx = coordx - sin(radians(angle)) * length
    new_coordy = coordy - cos(radians(angle)) * length
    return [new_coordx, new_coordy]


def draw_tree_base(image_size: tuple[int, int], base_coords: list[float],
                   state: str, alphabet: dict[str, float],
                   angles: dict[str, float], thickness: int,
                   length_reduction: float = 1, filename: str = "tree.png",
                   preview: bool = True,  ls: str = ''):

    image = Image.new('RGB', image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    coords: list[float] = base_coords
    angle: float = 0
    saved_coords: list[list[float]] = []
    saved_angles: list[float] = []

    for move in state:
        if move == '[':
            saved_coords.append(coords)
            saved_angles.append(angle)
        elif move == ']':
            coords = saved_coords.pop()
            angle = saved_angles.pop()
        if move == ls:
            draw.ellipse((coords[0], coords[1], coords[0] + 15,
                          coords[1] + 20), fill='green', outline=(0, 0, 0))
        if move in alphabet:
            newcoords = get_new_coords(coords[0], coords[1],
                                       angle, alphabet[move])
            draw.line((coords[0], coords[1], newcoords[0], newcoords[1]),
                      width=thickness, fill='black')
            coords = newcoords
        elif move in angles:
            angle += angles[move]

    image.save(filename, "PNG")
    if preview is True:
        image.show()


if __name__ == '__main__':
    tree = WMLLSystem('X', 1, {'F': 20, 'X': 0},  # noqa: F405
                      {'-': -15, '+': 22.5},
                      ['X->F-[[X]+X*]+F[+FX]-X*', 'F->FF'])
    tree.generate(5)
    draw_tree_base((2000, 2000), [1000, 1600], tree.state,
                   tree.alphabet, tree.angles, 3, ls='*')
