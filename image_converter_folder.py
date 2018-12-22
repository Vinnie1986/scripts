import argparse
from image_converter import convert
import os
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert files to API request objects')
    parser.add_argument('--folder', dest='folder', required=True, type=str, help='path to the file')
    args = parser.parse_args()

    for file in os.listdir(args.folder):
        setattr(args, 'input_file' ,os.path.join(args.folder, file))
        convert(args)