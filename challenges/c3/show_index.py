from __future__ import print_function

import os
from itertools import permutations

from PIL import Image, ImageFont, ImageDraw

images = [Image.open(os.path.join('shredded', '%s.png' % i)) for i in xrange(0, 27)]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))
draw = ImageDraw.Draw(new_im)
font = ImageFont.truetype("Roboto-Light.ttf", 8)

x_offset = 0
for i, im in enumerate(images):
    new_im.paste(im, (x_offset, 0))
    draw.text((x_offset, 5), str(i), (0, 0, 0), font=font)

    x_offset += im.size[0]

new_im.save("with_index.png")
