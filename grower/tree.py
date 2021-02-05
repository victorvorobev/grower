import time

from .branch import Trunk
from .exceptions import BranchIsDead


class Tree:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.x = int(width / 2)
        self.y = height
        self.image = [[" " for _ in range(width)] for _ in range(height)]
        self.branches = {hash(branch): branch for branch in (Trunk(self.x, self.y, self.height),)}

    def grow(self):
        while self.branches:
            branches = self.branches.copy()
            self._grow_branches(branches)
            self._split_branches(branches)
            self.display()
            time.sleep(0.1)

    def display(self):
        for row in self.image:
            print("".join(row))

    def _grow_branches(self, branches):
        for key, branch in branches.items():
            try:
                parts = branch.get_parts()
                for part in parts:
                    if self._part_in_borders(part):
                        self._insert_symbol(part)
            except BranchIsDead:
                del self.branches[key]

    def _split_branches(self, branches):
        for branch in branches.values():
            new_branch = branch.split()
            if new_branch:
                self.branches[hash(new_branch)] = new_branch

    def _part_in_borders(self, part):
        border_threshold = 0  # symbols from each border of the screen
        x_in_borders = border_threshold < part.x < self.width - border_threshold
        y_in_borders = border_threshold < part.y < self.height - border_threshold
        return x_in_borders and y_in_borders

    def _insert_symbol(self, part):
        self.image[part.y][part.x] = part.sym
