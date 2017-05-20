from collections import OrderedDict
from collections import defaultdict

from PIL import ImageOps
from pandas import DataFrame


def convert():
    from PIL import Image
    im = Image.open(r"C:\Users\vincentc.PHY\Desktop\kurt\p2\body_100px_15_colours.png").convert(
        'RGB')  # Can be many different formats.
    im = ImageOps.mirror(im)
    im = im.transpose(Image.ROTATE_90)
    pix = im.load()
    color_dict = OrderedDict()
    counter = 0
    color_counter = defaultdict(int)
    dataframe = DataFrame(index=range(im.size[0]), columns=range(im.size[1]))
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

    import collections
    # color_dict = sorted(color_dict)
    sorted_color_dict = collections.OrderedDict(sorted(color_dict.items(), reverse=True))
    dataframe = dataframe.applymap(lambda x: x * -1)
    for i, number in enumerate(sorted_color_dict.values(), start=1):
        dataframe = dataframe.applymap(lambda x: i if x * -1 == number else x)

    dataframe.to_csv(r"C:\Users\vincentc.PHY\Desktop\kurt\p2\body_100px_15_colours.csv", index=False, header=False,
                     sep=';')
    from PIL import Image

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

    im.save(r"C:\Users\vincentc.PHY\Desktop\kurt\p2\body_100px_15_colours_converter.png", "PNG")


if __name__ == '__main__':
    pass
