from PIL import Image


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
    def image(self):
        return self._generate_image()

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
        self._cell_len = 10
        self._define_backcolor()

    def _define_backcolor(self):
        colors = self.colors[:]
        colors.sort(key=lambda color: color[0] + color[1] + color[2], reverse=True)
        self._back_color = colors[0]

    def _generate_image(self):
        return Image.new(mode='RGB', size=self._get_image_size(), color=self.back_color)

    def _get_image_size(self):
        return self.width * self._cell_len, self.height * self._cell_len
