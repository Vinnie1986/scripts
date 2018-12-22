import argparse
import collections
import os
from collections import OrderedDict
from collections import defaultdict

from PIL import ImageOps, Image
from pandas import DataFrame


def get_image(input_file):
    im = Image.open(input_file).convert('RGB')  # Can be many different formats.
    im = ImageOps.mirror(im)
    im = im.transpose(Image.ROTATE_90)
    return im


def print_image(im, dataframe, color_dict, color_counter, pix, counter=0):
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

    return color_dict


def convert(args):

    input_file = args.input_file
    file_name, ext = os.path.splitext(input_file)

    im = get_image(input_file)

    pix = im.load()
    color_dict = OrderedDict()
    color_counter = defaultdict(int)
    dataframe = DataFrame(index=range(im.size[0]), columns=range(im.size[1]))
    counter = 0
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

    # color_dict = sorted(color_dict)
    sorted_color_dict = collections.OrderedDict(sorted(color_dict.items(), reverse=True))
    # color_dict = {[k[0],k[1],k[2]]:v for k,v in color_dict.iteritems()}
    # HILBERT
    #####################
    # color_list = color_dict.keys()
    # color_list.sort(
    #      key=lambda (r, g, b): hilbert.Hilbert_to_int([int(r * 255), int(g * 255), int(b * 255)]))
    # sorted_color_dict = {x: color_dict[x] for x in color_list}

    # STEP
    #######################
    # import math
    # import colorsys
    # def step(r, g, b, repetitions=1):
    #     lum = math.sqrt(.241 * r + .691 * g + .068 * b)
    #
    #     h, s, v = colorsys.rgb_to_hsv(r, g, b)
    #
    #     h2 = int(h * repetitions)
    #     lum2 = int(lum * repetitions)
    #     v2 = int(v * repetitions)
    #
    #     if h2 % 2 == 1:
    #         v2 = repetitions - v2
    #         lum = repetitions - lum
    #
    #     return (h2, lum, v2)
    # color_list = color_dict.keys()
    # color_list.sort(key=lambda (r, g, b): step(r, g, b, 8))
    # sorted_color_dict = {x: color_dict[x] for x in color_list}

    # import math
    # def lum(r, g, b):
    #     return math.sqrt(.241 * r + .691 * g + .068 * b)
    #
    # color_list = color_dict.keys()
    # color_list.sort(key=lambda rgb: lum(*rgb))
    # sorted_color_dict = {x: color_dict[x] for x in color_list}

    # def NN(A, start):
    #     """Nearest neighbor algorithm.
    #     A is an NxN array indicating distance between N locations
    #     start is the index of the starting location
    #     Returns the path and cost of the found solution
    #     """
    #     path = [start]
    #     cost = 0
    #     N = A.shape[0]
    #     mask = np.ones(N, dtype=bool)  # boolean values indicating which
    #     # locations have not been visited
    #     mask[start] = False
    #
    #     for i in range(N - 1):
    #         last = path[-1]
    #         next_ind = np.argmin(A[last][mask])  # find minimum of remaining locations
    #         next_loc = np.arange(N)[mask][next_ind]  # convert to original location
    #         path.append(next_loc)
    #         mask[next_loc] = False
    #         cost += A[last, next_loc]
    #
    #     return path, cost
    #
    #
    # from scipy.spatial import distance
    # import numpy as np
    #
    # colours_length = len(color_dict)
    # # Distance matrix
    # A = np.zeros([colours_length, colours_length])
    # for x in range(0, colours_length - 1):
    #     for y in range(0, colours_length - 1):
    #         A[x, y] = distance.euclidean(color_dict.keys()[x], color_dict.keys()[y])
    #
    # # Nearest neighbour algorithm
    # path, _ = NN(A, 0)
    #
    # # Final array
    # color_list = []
    # for i in path:
    #     color_list.append(color_dict.keys()[i])
    #
    # sorted_color_dict = {x: color_dict[x] for x in color_list}
    # color_list = color_dict.keys()
    # color_list.sort(key=lambda rgb: lum(*rgb))
    # sorted_color_dict = {x: color_dict[x] for x in color_list}
    dataframe = dataframe.applymap(lambda x: x * -1)
    color_dict = {}
    # the index of the color defines the "luminostory" *ahum*.
    # so if the first element was nr 5 -> it will become now nr 1 in the df and the color dict
    for i, colour in enumerate(sorted_color_dict.iteritems(), start=1):
        dataframe = dataframe.applymap(lambda x: i if x * -1 == colour[1] else x)
        # create a new color dict with the sorted colour ranging from 1 to x
        color_dict[colour[0]] = i

    color_dict = collections.OrderedDict(sorted(color_dict.items(), reverse=True))

    file_name_csv = file_name + '.csv'
    dataframe.to_csv(file_name_csv, index=False, header=False,
                     sep=';')

    fd = open(file_name_csv, 'a')
    fd.write('legende \n')
    fd.write('--------- \n')
    fd.write('dimensions : {} \n'.format(im.size))
    fd.write('')
    fd.write('{: >20} {: >20} {: >20} {: >20} {: >20} \n'.format('R', 'G', 'B', 'number', 'count'))
    for k, v in color_dict.iteritems():
        fd.write('{: >20} {: >20} {: >20} {: >20} {: >20} \n'.format(k[0], k[1], k[2], v, color_counter[k]))

    fd.close()
    number_of_colours = len(color_dict)
    LENGTH_SQUARE_SIDE = 50
    TOTAL_WIDTH = number_of_colours * LENGTH_SQUARE_SIDE
    TOTAL_HEIGHT = LENGTH_SQUARE_SIDE
    x_y = (TOTAL_WIDTH, TOTAL_HEIGHT)
    im = Image.new("RGB", (x_y[0], x_y[1]))
    pix = im.load()
    for y in range(x_y[1]):
        counter = 0
        for i, x in enumerate(range(x_y[0])):
            pix[x, y] = color_dict.keys()[counter]
            if i != 0 and i % LENGTH_SQUARE_SIDE == 0:
                counter += 1

    im.save(file_name + '_sorted_colours' + '.png', "PNG")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert files to API request objects')
    parser.add_argument('--input_file', dest='input_file', required=True, type=str, help='path to the file')
    args = parser.parse_args()
    convert(args)
