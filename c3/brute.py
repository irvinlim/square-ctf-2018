import os
from itertools import permutations

from PIL import Image
from pyzbar.pyzbar import decode

images = [Image.open(os.path.join('shredded', '%s.png' % i)) for i in xrange(0, 27)]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

for perm in permutations(range(27)):
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    data = decode(new_im)
    print(data)

    new_im.show()
    break
