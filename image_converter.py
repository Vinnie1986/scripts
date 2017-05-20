import argparse
import os
from collections import OrderedDict
from collections import defaultdict

from PIL import ImageOps, Image
from pandas import DataFrame

import hilbert

def get_image(input_file):
    im = Image.open(input_file).convert('RGB')  # Can be many different formats.
    im = ImageOps.mirror(im)
    im = im.transpose(Image.ROTATE_90)
    return im


def print_image(im, dataframe, color_dict, counter = 0):
    print 'printing image : '
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pix[i, j] not in color_dict.keys():
                counter += 1
                color_dict[pix[i, j]] = counter
            color_counter[pix[i, j]] += 1
            print color_dict[pix[i, j]],
            dataframe.loc[i, j] = color_dict[pix[i, j]]
        print ''

    print 'legende'
    print '---------'
    print 'dimensions : {}'.format(im.size)
    print ''
    print '{: >20} {: >20} {: >20} {: >20} {: >20}'.format('R', 'G', 'B', 'number', 'count')
    for k, v in color_dict.iteritems():
        print '{: >20} {: >20} {: >20} {: >20} {: >20}'.format(k[0], k[1], k[2], v, color_counter[k])

def convert():
    parser = argparse.ArgumentParser(description='Convert files to API request objects')
    parser.add_argument('--input_file', dest='input_file', required=True, type=str, help='path to the file')
    args = parser.parse_args()
    input_file = args.input_file
    file_name, ext = os.path.splitext(input_file)

    im = get_image(input_file)

    pix = im.load()
    color_dict = OrderedDict()
    counter = 0
    color_counter = defaultdict(int)
    dataframe = DataFrame(index=range(im.size[0]), columns=range(im.size[1]))

    print_image(im, color_dict, counter = 0)


    # color_dict = sorted(color_dict)
    # sorted_color_dict = collections.OrderedDict(sorted(color_dict.items(), reverse=True))
    sorted_color_dict = color_dict.items().sort(
        key=lambda (r, g, b): hilbert.Hilbert_to_int([int(r * 255), int(g * 255), int(b * 255)]))

    dataframe = dataframe.applymap(lambda x: x * -1)
    for i, number in enumerate(sorted_color_dict.values(), start=1):
        dataframe = dataframe.applymap(lambda x: i if x * -1 == number else x)

    dataframe.to_csv(file_name + '.csv', index=False, header=False,
                     sep=';')

    number_of_colours = len(sorted_color_dict)
    LENGTH_SQUARE_SIDE = 50
    TOTAL_WIDTH = number_of_colours * LENGTH_SQUARE_SIDE
    TOTAL_HEIGHT = LENGTH_SQUARE_SIDE
    x_y = (TOTAL_WIDTH, TOTAL_HEIGHT)
    im = Image.new("RGB", (x_y[0], x_y[1]))
    pix = im.load()
    for y in range(x_y[1]):
        counter = 0
        for i, x in enumerate(range(x_y[0])):
            pix[x, y] = sorted_color_dict.keys()[counter]
            if i != 0 and i % LENGTH_SQUARE_SIDE == 0:
                counter += 1

    im.save(file_name + '_sorted_colours' + '.png', "PNG")


if __name__ == '__main__':
    convert()
