import argparse
import glob
import io
import os
from PIL import Image, ImageFont, ImageDraw


# Default data paths
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LABEL_FILE = os.path.join(SCRIPT_PATH, 'labels/2350-common-hangul.txt')
DEFAULT_FONTS_DIR = os.path.join(SCRIPT_PATH, 'fonts')
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'output')


# Width and height of the resulting image.
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


# Generate font image using label file
def lbl2img(lbl_dir, fonts_dir, output_dir):

    with io.open(lbl_dir, 'r', encoding='utf-8') as f:
        labels = f.read().splitlines()
    
    image_dir = os.path.join(output_dir)
    if not os.path.exists(image_dir):
        os.makedirs(os.path.join(image_dir))

    # Get a list of the fonts.
    fonts = glob.glob(os.path.join(fonts_dir, '*.ttf'))

    total_count = 0
    font_count = 0
    char_no = 0
    
    for character in labels:

        char_no += 1

        for font in fonts:
            total_count += 1
                
            image = Image.new('RGB', (IMAGE_WIDTH,IMAGE_HEIGHT), (255, 255, 255))
            w, h = image.size
                
            drawing = ImageDraw.Draw(image)
            font = ImageFont.truetype(font, 170)
            
            box = None
            new_box = drawing.textbbox((0, 0), character, font)
                
            new_w = new_box[2] - new_box[0]
            new_h = new_box[3] - new_box[1]
                
            box = new_box
            w = new_w
            h = new_h
                
            x = (IMAGE_WIDTH - w)//2 - box[0]
            y = (IMAGE_HEIGHT - h)//2 - box[1]
                
            drawing.text((x,y), character, fill=(0), font=font)
            file_string = '{}_{}.png'.format(font,character)
            file_path = os.path.join(image_dir, file_string)
            image.save(file_path, 'PNG')

        font_count = 0
    char_no = 0

    print('Finished generating {} images.'.format(total_count))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--lbl-dir', type=str, dest='lbl_dir', default=DEFAULT_LABEL_FILE, help='File containing newline delimited labels.')
    parser.add_argument('--fonts-dir', type=str, dest='fonts_dir', default=DEFAULT_FONTS_DIR, help='Directory of ttf fonts to use.')
    parser.add_argument('--output-dir', type=str, dest='output_dir', default=DEFAULT_OUTPUT_DIR, help='Output directory to store generated images.')

    args = parser.parse_args()

    lbl2img(args.lbl_dir, args.fonts_dir, args.output_dir)