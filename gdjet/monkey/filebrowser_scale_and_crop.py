# -*- coding: utf-8 -*-

import Image

def scale_and_crop_fix(im, width, height, opts):
    """
    Scale and Crop. And Extent.
    """
    x, y   = [float(v) for v in im.size]
    if width:
        xr = float(width)
    else:
        xr = float(x*height/y)
    if height:
        yr = float(height)
    else:
        yr = float(y*width/x)
    if 'crop' in opts:
        r = max(xr/x, yr/y)
    else:
        r = min(xr/x, yr/y)

    if r < 1.0 or (r > 1.0 and 'upscale' in opts):
        im = im.resize((int(x*r), int(y*r)), resample=Image.ANTIALIAS)
    if ('extent' in opts) and (r < 1.0):
        px = width - im.size[0]
        if px>0:
            im2 = Image.new( im.mode, (width, height))
            im2.paste( im, ( px/2, 0 ))
            im = im2
        py = height - im.size[1]
        if py>0:
            im2 = Image.new( im.mode, (width, height))
            im2.paste( im, ( 0, py/2 ))
            im = im2
    if 'crop' in opts:
        x, y   = [float(v) for v in im.size]
        ex, ey = (x-min(x, xr))/2, (y-min(y, yr))/2
        if ex or ey:
            im = im.crop((int(ex), int(ey), int(x-ex), int(y-ey)))
    return im

try:
    from filebrowser import functions
    functions.scale_and_crop = scale_and_crop_fix
    # functions.convert_filename = convert_filename
except:
    pass