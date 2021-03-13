from PIL import Image
from PIL.ImageDraw import Draw
from .nonogram import Nonogram
from .section import Section


class NonogramRenderer:

    def __init__(self, nonogram: Nonogram):
        self._nonogram = nonogram

    @property
    def nonogram(self):
        return self._nonogram

    def render(self,
               cell_len=3,
               grid_width=2,
               show_solution=False):

        size = NonogramRenderer._get_image_size(self.nonogram.width,
                                                self.nonogram.height,
                                                self.nonogram.horizontal_sections,
                                                self.nonogram.vertical_sections,
                                                cell_len,
                                                grid_width)

        image = Image.new(mode='RGB', size=size, color=self.nonogram.back_color)
        draw = Draw(image)

        self._draw_grid(draw, size, cell_len, grid_width)

        return image

    def _get_nonogram_origin(self, cell_len):
        h_sections_count = NonogramRenderer._get_max_sections_len(self.nonogram.horizontal_sections)
        v_sections_count = NonogramRenderer._get_max_sections_len(self.nonogram.vertical_sections)
        x = h_sections_count * cell_len
        y = v_sections_count * cell_len
        return x, y

    def _draw_grid(self, draw: Draw, size: tuple, cell_len: int, grid_width: int):
        origin = self._get_nonogram_origin(cell_len)
        for x in range(self.nonogram.width + 1):
            x_start = origin[0] + x * cell_len + x * grid_width
            rectangle = [(x_start, 0),
                         (x_start + grid_width - 1, size[1])]
            draw.rectangle(rectangle, fill='black', width=0)

        for y in range(self.nonogram.height + 1):
            y_start = origin[1] + y * cell_len + y * grid_width
            rectangle = [(0, y_start),
                         (size[0], y_start + grid_width - 1)]
            draw.rectangle(rectangle, fill='black', width=0)

    @staticmethod
    def _get_dimension_len(length, sections, cell_len, grid_width):
        max_sect_len = NonogramRenderer._get_max_sections_len(sections)
        return (length + max_sect_len) * cell_len + (length + 1) * grid_width

    @staticmethod
    def _get_image_size(nonogram_width: int,
                        nonogram_heigth: int,
                        horizontal_sections: list[list[Section]],
                        vertical_sections: list[list[Section]],
                        cell_len: int,
                        grid_width: int):

        width = NonogramRenderer._get_dimension_len(nonogram_width, horizontal_sections, cell_len, grid_width)
        height = NonogramRenderer._get_dimension_len(nonogram_heigth, vertical_sections, cell_len, grid_width)
        return width, height

    @staticmethod
    def _get_max_sections_len(lines_of_sections: list[list[Section]]) -> int:
        lines = list(lines_of_sections)
        return max(list(map(lambda line: len(line), lines_of_sections)))
