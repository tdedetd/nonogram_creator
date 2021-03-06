import os
from PIL import Image
from .utils import endswith, remove_dublicates
from .nonogram import Nonogram


IN_DIRECTORY = 'in'
PICTURE_EXTENSIONS = ['.png', '.bmp']


def main():
    files = [f for f in os.listdir(IN_DIRECTORY) if endswith(f, PICTURE_EXTENSIONS)]
    for f in files:
        path = os.path.join(IN_DIRECTORY, f)
        image = Image.open(path)
        handle(image)


def handle(image: Image) -> None:
    pixels = list(image.getdata())
    colors: list[tuple] = remove_dublicates(pixels)
    nonogram = Nonogram(colors)


if __name__ == '__main__':
    main()
