import random
from typing import List

from .constants import Symbols, Directions, brown_colors, green_colors
from .exceptions import BranchIsDead
from .utils import Step, Part


class BranchInterface:
    def __init__(self, x: int, y: int, limit: int, direction: Directions = None):
        """
        Common interface for trunk and branches of the tree
        Args:
            x: origin of the branch. Numeration goes from left to right
            y: origin of the branch. Numeration goes from top to bottom
            limit: how long the branch should grow (cycles), should be less than image height
            direction: meaningful only for branch, should be instance of Directions
        """
        self.x, self.y = x, y
        self.live_length = self.max_live_length = random.randint(int(limit / 2), int(limit))

    def get_parts(self) -> List[Part]:
        """
        Get list of new parts for the image
        Returns:
            list of Parts
        """
        if not self.live_length:
            raise BranchIsDead
        self.live_length -= 1

    def split(self):
        """
        Creates new branch from current place in the branch.
        Returns:
            instance of new Branch
        """


class Trunk(BranchInterface):
    DIRECTIONS = (Directions.RIGHT, Directions.UP, Directions.LEFT)
    TREND_SWITCH_WEIGHTS = {  # right, up, left
        Directions.RIGHT: (0.4, 0.5, 0.05),
        Directions.UP: (0.1, 0.8, 0.1),
        Directions.LEFT: (0.05, 0.5, 0.4)
    }
    WOOD_SYMBOLS = (Symbols.wood_r, Symbols.wood_u, Symbols.wood_l)
    WOOD_SYMBOLS_WEIGHTS = {  # right, up, left
        Directions.RIGHT: (0.5, 0.4, 0.05),
        Directions.UP: (0.25, 0.5, 0.25),
        Directions.LEFT: (0.05, 0.4, 0.5)
    }
    STEP = {
        Directions.RIGHT: Step(dx=1, dy=-1),
        Directions.UP: Step(dx=0, dy=-1),
        Directions.LEFT: Step(dx=-1, dy=-1)
    }

    def __init__(self, x, y, limit, direction=None):
        super().__init__(x, y, limit, direction)
        self.direction = random.choice(self.DIRECTIONS)
        self.max_width = 4

    def get_parts(self):
        super().get_parts()

        self._grow()
        parts = self._get_trunk_parts()
        return parts

    def split(self):
        if random.randint(0, 4):
            return None
        if self.direction is Directions.LEFT:
            new_branch_direction = Directions.RIGHT
        elif self.direction is Directions.RIGHT:
            new_branch_direction = Directions.LEFT
        else:
            new_branch_direction = random.choice((Directions.LEFT, Directions.RIGHT))
        return Branch(self.x, self.y, self.live_length, new_branch_direction)

    def _get_trunk_parts(self):
        current_width = int(round(self.live_length * self.max_width / self.max_live_length, 0))
        parts = []
        for sym_x in range(-1, current_width - 1):
            x = self.x + sym_x
            symbol, color = self._get_wood()
            parts.append(Part(x=x, y=self.y, sym=symbol, color=color))

        return parts

    def _switch_trend(self):
        self.direction = random.choices(self.DIRECTIONS, weights=self.TREND_SWITCH_WEIGHTS[self.direction])[0]

    def _grow(self):
        self._switch_trend()

        step = self.STEP[self.direction]
        self.x += step.dx
        self.y += step.dy

    def _get_wood(self):
        symbol = random.choices(self.WOOD_SYMBOLS, weights=self.WOOD_SYMBOLS_WEIGHTS[self.direction])[0]
        return symbol, brown_colors


class Branch(BranchInterface):
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
        super().__init__(x, y, limit, direction)
        self.direction = random.choice((Directions.RIGHT, Directions.LEFT)) \
            if not direction \
            else direction
        self.steps = self.LEFT_STEPS if self.direction is Directions.LEFT else self.RIGHT_STEPS

    def get_parts(self):
        super().get_parts()

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
