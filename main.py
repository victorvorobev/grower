import shutil

from grower.tree import Tree


def main():
    width, height = shutil.get_terminal_size()
    tree = Tree(height=height, width=width)
    tree.grow()


if __name__ == '__main__':
    main()
