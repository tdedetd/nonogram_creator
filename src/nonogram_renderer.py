import math

from PIL import Image, ImageFont
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
               bold_grid_width=4,
               cell_len=40,
               grid_section_size=5,
               grid_width=2,
               show_solution=False):

        size = NonogramRenderer._get_image_size(self.nonogram.width,
                                                self.nonogram.height,
                                                self.nonogram.horizontal_sections,
                                                self.nonogram.vertical_sections,
                                                cell_len,
                                                grid_width,
                                                bold_grid_width,
                                                grid_section_size)

        image = Image.new(mode='RGB', size=size, color=self.nonogram.back_color)
        draw = Draw(image)
        origin = self._get_nonogram_origin(cell_len)

        self._draw_grid(draw, origin, size, cell_len, grid_width, bold_grid_width, grid_section_size)
        self._draw_sections(draw, origin, cell_len, grid_width, bold_grid_width, grid_section_size)

        if show_solution:
            self._draw_solution(draw, origin, cell_len, grid_width, bold_grid_width, grid_section_size)

        return image

    def _get_nonogram_origin(self, cell_len):
        h_sections_count = NonogramRenderer._get_max_sections_count(self.nonogram.horizontal_sections)
        v_sections_count = NonogramRenderer._get_max_sections_count(self.nonogram.vertical_sections)
        x = h_sections_count * cell_len
        y = v_sections_count * cell_len
        return x, y

    def _draw_grid(self,
                   draw: Draw,
                   origin: tuple,
                   size: tuple,
                   cell_len: int,
                   grid_width: int,
                   bold_grid_width: int,
                   grid_section_size: int):

        cur_coord = origin[0]
        for x in range(self.nonogram.width + 1):
            bold = x > 0 and x < self.nonogram.width and x % grid_section_size == 0
            cur_grid_width = bold_grid_width if bold else grid_width

            rect = [(cur_coord, 0),
                    (cur_coord + cur_grid_width - 1, size[1])]
            draw.rectangle(rect, fill='black', width=0)
            cur_coord += cur_grid_width + cell_len

        cur_coord = origin[1]
        for y in range(self.nonogram.height + 1):
            bold = y > 0 and y < self.nonogram.height and y % grid_section_size == 0
            cur_grid_width = bold_grid_width if bold else grid_width

            rect = [(0, cur_coord),
                    (size[0], cur_coord + cur_grid_width - 1)]
            draw.rectangle(rect, fill='black', width=0)
            cur_coord += cur_grid_width + cell_len

    def _draw_section(self, draw: Draw, font, section: Section, coords: tuple):
        x_diff = 0.4 * font.size if section.length < 10 else 0.08 * font.size
        label_color = (0, 0, 0) if self.nonogram.mono else section.label_color
        draw.text((coords[0] + x_diff, coords[1] + 0.1 * font.size), str(section.length), font=font, fill=label_color)

    def _draw_sections(self,
                       draw: Draw,
                       origin: tuple,
                       cell_len: int,
                       grid_width: int,
                       bold_grid_width: int,
                       grid_section_size: int):

        font_size = int(0.8 * cell_len)
        font = ImageFont.truetype(font='Arial.ttf', size=font_size)
        cell_len_sub_1 = cell_len - 1

        cur_coord = origin[0]
        for x, line in enumerate(self.nonogram.vertical_sections):
            bold = x > 0 and x < self.nonogram.width and x % grid_section_size == 0
            cur_coord += bold_grid_width if bold else grid_width

            sections_count = len(line)
            for index, section in enumerate(line):
                y_start = origin[1] - (sections_count - index) * cell_len
                rect = [(cur_coord, y_start), (cur_coord + cell_len_sub_1, y_start + cell_len_sub_1)]
                if not self.nonogram.mono:
                    draw.rectangle(rect, fill=section.color, width=0)
                self._draw_section(draw, font, section, (cur_coord, y_start))

            cur_coord += cell_len

        cur_coord = origin[1]
        for y, line in enumerate(self.nonogram.horizontal_sections):
            bold = y > 0 and y < self.nonogram.height and y % grid_section_size == 0
            cur_coord += bold_grid_width if bold else grid_width

            sections_count = len(line)
            for index, section in enumerate(line):
                x_start = origin[0] - (sections_count - index) * cell_len
                rect = [(x_start, cur_coord), (x_start + cell_len_sub_1, cur_coord + cell_len_sub_1)]
                if not self.nonogram.mono:
                    draw.rectangle(rect, fill=section.color, width=0)
                self._draw_section(draw, font, section, (x_start, cur_coord))

            cur_coord += cell_len

    def _draw_solution(self,
                       draw: Draw,
                       origin: tuple,
                       cell_len: int,
                       grid_width: int,
                       bold_grid_width: int,
                       grid_section_size: int):

        image = self.nonogram.image
        px = image.load()

        cur_x = origin[0]
        for x in range(image.width):
            bold = x > 0 and x < image.width and x % grid_section_size == 0
            cur_x += bold_grid_width if bold else grid_width

            cur_y = origin[1]
            for y in range(image.height):
                bold = y > 0 and y < image.height and y % grid_section_size == 0
                cur_y += bold_grid_width if bold else grid_width
                rect = [(cur_x + x, cur_y + y), (cur_x + x + cell_len - 1, cur_y + y + cell_len - 1)]
                draw.rectangle(rect, fill=px[x, y], width=0)
                cur_y += cell_len - 1

            cur_x += cell_len - 1

    @staticmethod
    def _get_dimension_len(length: int,
                           sections: list[list[Section]],
                           cell_len: int,
                           grid_width: int,
                           bold_grid_width: int,
                           grid_section_size: int):

        max_sect_len = NonogramRenderer._get_max_sections_count(sections)
        grid_sect_dividers_count = math.ceil(length / grid_section_size) - 1
        grid_total_width = (length - grid_sect_dividers_count + 1) * grid_width + grid_sect_dividers_count * bold_grid_width

        return (length + max_sect_len) * cell_len + grid_total_width

    @staticmethod
    def _get_image_size(nonogram_width: int,
                        nonogram_heigth: int,
                        horizontal_sections: list[list[Section]],
                        vertical_sections: list[list[Section]],
                        cell_len: int,
                        grid_width: int,
                        bold_grid_width: int,
                        grid_section_size: int):

        width = NonogramRenderer._get_dimension_len(nonogram_width, horizontal_sections, cell_len, grid_width, bold_grid_width, grid_section_size)
        height = NonogramRenderer._get_dimension_len(nonogram_heigth, vertical_sections, cell_len, grid_width, bold_grid_width, grid_section_size)
        return width, height

    @staticmethod
    def _get_max_sections_count(lines_of_sections: list[list[Section]]) -> int:
        lines = list(lines_of_sections)
        return max(list(map(lambda line: len(line), lines_of_sections)))
