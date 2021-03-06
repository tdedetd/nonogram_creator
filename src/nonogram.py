class Nonogram:

    @property
    def back_color(self):
        return self._back_color

    @property
    def colors(self):
        return self._colors

    @property
    def height(self):
        return self._height

    @property
    def mono_color(self):
        return len(self.colors) <= 2

    @property
    def width(self):
        return self._width

    def __init__(self, width: int, height: int, colors: list[tuple]):
        self._width = width
        self._height = height
        self._colors = colors
        self._define_backcolor()

    def _define_backcolor(self):
        colors = self.colors[:]
        colors.sort(key=lambda color: color[0] + color[1] + color[2], reverse=True)
        self._back_color = colors[0]
