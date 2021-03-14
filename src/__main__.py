import argparse, os
from PIL import Image
from .utils import endswith
from .nonogram import Nonogram
from .nonogram_renderer import NonogramRenderer


IN_DIRECTORY = 'in'
OUT_DIRECTORY = 'out'
PICTURE_EXTENSIONS = ['.png', '.bmp']


def main(args: dict):
    if not os.path.exists(OUT_DIRECTORY):
        os.makedirs(OUT_DIRECTORY)

    files = [f for f in os.listdir(IN_DIRECTORY) if endswith(f, PICTURE_EXTENSIONS)]
    for f in files:
        path = os.path.join(IN_DIRECTORY, f)
        image = Image.open(path)
        print('%s (%ix%i)' % (f, image.width, image.height))

        res_image = handle(image, args)
        res_image.save(os.path.join(OUT_DIRECTORY, f))

    if len(files) == 0:
        print('No images found')


def handle(image: Image, args: dict) -> Image:
    nonogram = Nonogram(image)
    return NonogramRenderer(nonogram).render(bold_grid_width=args['bold_grid_width'],
                                             cell_len=args['cell_len'],
                                             grid_section_size=args['grid_section_size'],
                                             grid_width=args['grid_width'],
                                             show_solution=args['show_solution'])


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Parser for command line args')
    argparser.add_argument('--bold-grid-width', default=4, help='Width of grid between sections of grid', type=int)
    argparser.add_argument('--cell-len', default=40, help='Length of cells in pixels', type=int)
    argparser.add_argument('--grid-section-size', default=5, help='Size of grid sections in cells', type=int)
    argparser.add_argument('--grid-width', default=2, help='Width of grid', type=int)
    argparser.add_argument('--show-solution', default=False, help='If need to render solution', type=bool)
    args = argparser.parse_args()
    main(args.__dict__)
