import os
from PIL import Image
from .utils import endswith
from .nonogram import Nonogram


IN_DIRECTORY = 'in'
OUT_DIRECTORY = 'out'
PICTURE_EXTENSIONS = ['.png', '.bmp']


def main():
    if not os.path.exists(OUT_DIRECTORY):
        os.makedirs(OUT_DIRECTORY)

    files = [f for f in os.listdir(IN_DIRECTORY) if endswith(f, PICTURE_EXTENSIONS)]
    for f in files:
        path = os.path.join(IN_DIRECTORY, f)
        image = Image.open(path)
        print('%s (%ix%i)' % (f, image.size[0], image.size[1]))

        res_image = handle(image)
        res_image.save(os.path.join(OUT_DIRECTORY, f))

    if len(files) == 0:
        print('No images found')


def handle(image: Image) -> Image:
    nonogram = Nonogram(image)
    return nonogram.generate_template()


if __name__ == '__main__':
    main()
