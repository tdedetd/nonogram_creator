class Section:

    __slots__ = ('_color', '_length')

    def __init__(self, color: tuple, length: int):
        self._color = color
        self._length = length

    @property
    def color(self):
        return self._color

    @property
    def length(self):
        return self._length
