from typing import NoReturn
from dataclasses import dataclass, field
from rule import *


@dataclass(frozen=False)
class LSystem:
    axiom: str
    alphabet: dict[str, float]
    angles: dict[str, float]
    rules: list[str]
    state: str = field(init=False)

    def __post_init__(self):
        self.state = self.axiom
