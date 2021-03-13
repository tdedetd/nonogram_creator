from PIL import Image
from .section import Section
from .utils import remove_dublicates


class Nonogram:

    __slots__ = ('_back_color',
                 '_horisontal_sections',
                 '_image',
                 '_mono',
                 '_vertical_sections')

    def __init__(self, image: Image):
        self._image = image
        self._define_backcolor()
        self._calc_horisontal_sections()
        self._calc_vertical_sections()

    @property
    def back_color(self):
        return self._back_color

    @property
    def height(self):
        """
        Height of original image in pixels
        """
        return self.image.height

    @property
    def horizontal_sections(self) -> list[list[Section]]:
        return self._horisontal_sections

    @property
    def image(self):
        return self._image

    @property
    def mono(self) -> bool:
        """
        If nonogram has 2 or less different colors
        """
        return self._mono

    @property
    def vertical_sections(self) -> list[list[Section]]:
        return self._vertical_sections

    @property
    def width(self):
        """
        Width of original image in pixels
        """
        return self.image.width

    def _calc_horisontal_sections(self):
        pixels = self.image.load()
        lines = []

        for y in range(self.height):
            lines.append([pixels[x, y] for x in range(self.width)])

        self._horisontal_sections = list(map(lambda line: self._get_sections(line), lines))

    def _calc_vertical_sections(self):
        pixels = self.image.load()
        lines = []

        for x in range(self.width):
            lines.append([pixels[x, y] for y in range(self.height)])

        self._vertical_sections = list(map(lambda line: self._get_sections(line), lines))

    def _define_backcolor(self):
        pixels = list(self.image.getdata())
        colors = remove_dublicates(pixels)
        colors.sort(key=lambda color: color[0] + color[1] + color[2], reverse=True)

        self._mono = len(colors) <= 2
        self._back_color = colors[0]

    def _get_sections(self, colors: list) -> list[Section]:
        sections = []
        previous_color = None
        length = 0

        for color in colors:
            if previous_color is not None and previous_color != color:
                if previous_color != self.back_color:
                    sections.append(Section(color=previous_color, length=length))
                length = 0

            length += 1
            previous_color = color

        if previous_color != self.back_color:
            sections.append(Section(color=previous_color, length=length))

        return sections
