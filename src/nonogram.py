from PIL import Image
from .utils import remove_dublicates


class Nonogram:

    @property
    def back_color(self):
        return self._back_color

    @property
    def colors(self):
        return self._colors

    @property
    def height(self):
        """
        Height of image in number of cells
        """
        return self._height

    @property
    def image(self):
        return self._image()

    @property
    def mono_color(self) -> bool:
        return len(self.colors) <= 2

    @property
    def width(self):
        """
        Width of image in number of cells
        """
        return self._width

    def __init__(self, image: Image):
        self._width = image.size[0]
        self._height = image.size[1]
        self._cell_len = 10
        self._image = image

        pixels = list(image.getdata())
        self._colors = remove_dublicates(pixels)
        self._define_backcolor()

    def generate_template(self):
        return Image.new(mode='RGB', size=self._get_image_size(), color=self.back_color)

    def _define_backcolor(self):
        colors = self.colors[:]
        colors.sort(key=lambda color: color[0] + color[1] + color[2], reverse=True)
        self._back_color = colors[0]

    def _get_image_size(self):
        return self.width * self._cell_len, self.height * self._cell_len
