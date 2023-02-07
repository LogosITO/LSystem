from PIL import Image
from PIL import ImageDraw
from math import sin, cos, radians
from typing import Any
from dataclasses import asdict
from lsystem import *


def draw_tree_base(image_size: tuple[int, int], base_coords: list[float],
                   state: str, alphabet: dict[str, int], angles: dict[str, float], 
                   saving_filename: str = "tree.png",preview: bool = True):

    image = Image.new('RGB', image_size)
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
        if move in alphabet:
            new_coords: list[float] = [0, 0]
            xlen: float = sin(radians(angle)) * alphabet[move]
            ylen: float = cos(radians(angle)) * alphabet[move]
            new_coords[0] = coords[0] - xlen
            new_coords[1] = coords[1] - ylen
            draw.line((coords[0], coords[1], new_coords[0], new_coords[1]))
            coords = new_coords
        elif move in angles:
            angle -= angles[move]

    image.save(saving_filename, "PNG")
    if preview is True:
        image.show()

if __name__ == '__main__':
    tree = LSystem('F', 1, {'F': 10, 'A': 5}, {'-': 30, '+': 30, ')': 105}, ['F->F[F+FA)A]+A', 'A->F--FA+F'])
    tree.generate(5)
    draw_tree_base((800, 400), [400, 200], tree.state, tree.alphabet, tree.angles)