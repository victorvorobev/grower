from sty import fg, Style, RgbFg

# It's necessary to initialise colors by adding it to fg

fg.brown_1 = Style(RgbFg(191, 92, 0))
fg.brown_2 = Style(RgbFg(150, 84, 23))
fg.brown_3 = Style(RgbFg(117, 60, 7))
brown_colors = (
    fg.brown_1, fg.brown_2, fg.brown_3
)

fg.green_1 = Style(RgbFg(34, 139, 34))
fg.green_2 = Style(RgbFg(0, 128, 0))
fg.green_3 = Style(RgbFg(0, 100, 0))
green_colors = (
    fg.green_1, fg.green_2, fg.green_3,
)


class Symbols:
    leaf = "&"
    wood_u = "|"
    wood_h = "~"
    wood_r = "/"
    wood_l = "\\"


class Directions:
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"
