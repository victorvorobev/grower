from dataclasses import dataclass
from random import choice

from sty import fg


@dataclass
class Step:
    dx: int
    dy: int
    sym: str = None


@dataclass
class Part:
    x: int
    y: int
    sym: str
    color: 'typing.Any' = None

    def __post_init__(self):
        if self.color:
            self.add_color_to_sym()

    def add_color_to_sym(self):
        if isinstance(self.color, (list, tuple)):
            self.color = choice(self.color)
        self.sym = self.color + self.sym + fg.rs
