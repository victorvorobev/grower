import random

from .constants import Symbols, Directions, brown_colors, green_colors
from .exceptions import BranchIsDead
from .utils import Step, Part


class Branch:
    RIGHT_STEPS = (
        Step(sym=Symbols.wood_u, dx=0, dy=-1),
        Step(sym=Symbols.wood_r, dx=1, dy=-1),
        Step(sym=Symbols.wood_h, dx=1, dy=0),
        Step(sym=Symbols.wood_l, dx=1, dy=1)
    )
    LEFT_STEPS = (
        Step(sym=Symbols.wood_u, dx=0, dy=-1),
        Step(sym=Symbols.wood_l, dx=-1, dy=-1),
        Step(sym=Symbols.wood_h, dx=-1, dy=0),
        Step(sym=Symbols.wood_r, dx=-1, dy=1)
    )

    def __init__(self, x, y, limit, direction=None):
        self.x, self.y = x, y
        self.live_length = self.max_live_length = random.randint(int(limit / 2), int(limit))
        self.direction = random.choice((Directions.RIGHT, Directions.LEFT)) \
            if not direction \
            else direction
        self.steps = self.LEFT_STEPS if self.direction is Directions.LEFT else self.RIGHT_STEPS

    def get_parts(self):
        if not self.live_length:
            raise BranchIsDead
        self.live_length -= 1

        parts = [self._get_branch_part(), *self._get_leaves()]
        return parts

    def _get_branch_part(self):
        step = random.choices(self.steps, weights=(0.3, 0.35, 0.3, 0.05))[0]
        sym, dx, dy = step.sym, step.dx, step.dy
        self.x += dx
        self.y += dy
        return Part(x=self.x, y=self.y, sym=sym, color=brown_colors)

    def split(self):
        if self.live_length > self.max_live_length / 2:
            return None
        if random.randint(0, 10):
            return None
        new_branch_direction = Directions.LEFT if self.direction is Directions.RIGHT else Directions.LEFT
        return Branch(self.x, self.y, self.live_length, direction=new_branch_direction)

    def _get_leaves(self):
        num_leaves = 8 - self.live_length
        if num_leaves < 0:
            num_leaves = 1
        return [Part(self.x + random.randint(-1, 1), self.y + random.randint(-1, 1), Symbols.leaf, color=green_colors)
                for _ in range(random.randint(0, num_leaves))]
