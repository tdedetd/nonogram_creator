class Section:

    __slots__ = ('_color', '_length')

    def __init__(self, color: tuple, length: int):
        self._color = color
        self._length = length

    @property
    def color(self):
        return self._color

    @property
    def label_color(self):
        avg = (self.color[0] + self.color[1] + self.color[2]) / 3
        return (0, 0, 0) if avg > 127 else (255, 255, 255)

    @property
    def length(self):
        return self._length
