from PIL import Image
from PIL import ImageDraw
from math import sin, cos, radians
from typing import Any


def draw(image_size: tuple[int, int], base_coords: list[float],
         lsystem: dict[str, Any], saving_filename: str = "tree.png",
         preview: bool = True):

    image = Image.new('RGB', image_size)
    draw = ImageDraw.Draw(image)
    coords: list[float] = base_coords
    angle: float = 0
    delta_angle: float = lsystem['angle']
    saved_coords: list[list[float]] = []
    saved_angles: list[float] = []

    for move in lsystem['state']:
        if move == '[':
            saved_coords.append(coords)
            saved_angles.append(angle)
        elif move == ']':
            coords = saved_coords.pop()
            angle = saved_angles.pop()
        elif move == '+':
            angle -= delta_angle
        elif move == '-':
            angle += delta_angle
        if move in lsystem['alphabet']:
            new_coords: list[float] = [0, 0]
            xlen: float = sin(radians(angle)) * lsystem['alphabet'][move]
            ylen: float = cos(radians(angle)) * lsystem['alphabet'][move]
            new_coords[0] = coords[0] - xlen
            new_coords[1] = coords[1] - ylen
            draw.line((coords[0], coords[1], new_coords[0], new_coords[1]))
            coords = new_coords

    image.save(saving_filename, "PNG")
    if preview is True:
        image.show()
