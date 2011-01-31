# -*- coding: utf-8 -*-
"""
@author: g4b

Copyright (C) 2009 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

def url_prefix( mod = 'G4BTOOLS', default = '/' ):
    """
        very handy function to give you any prefix for PREFIX settings
        variable. removes starting /, to be compatible with regexes!
    """
    from django.conf import settings
    prefix = getattr(
            getattr( settings, 'PREFIX', {} ),
            mod,
            default )
    if prefix.startswith('/'):
        prefix = prefix[1:]
    return prefix
            

def get_aspect_ratio(size_x, size_y, max_x, max_y):
    im_aspect = float(size_x)/float(size_y)
    out_aspect = float(max_x)/float(max_y)
    if im_aspect >= out_aspect:
        return (max_x, int((float(max_x)/im_aspect) + 0.5))
    else:
        return (int((float(max_y)*im_aspect) + 0.5), max_y)

def image_resize_aspect(image, max_size, method = 1):
    """ returns an image object resized by aspect ratio """
    return image.resize(get_aspect_ratio(image.size[0], image.size[1], max_size[0], max_size[1]), method)

def create_thumbnail(filename = None, width = 120, height = 80, extension = "jpg", location = "./thumb/"):
    import os
    import Image
    if filename:
        try:
            os.makedirs(location)
        except:
            pass
        save_to = ""
        try:
            if not extension.startswith('.'):
                extension = '.' + extension.lower()
            image = image_resize_aspect( Image.open(filename), 
                                         (width, height), 
                                         Image.ANTIALIAS )
            thumb_filename = os.path.split(os.path.splitext(filename)[0])[1]
            save_to = location + thumb_filename + extension
            image.save(save_to)
        except IOError, e:
            pass
            #log("IOError in saving thumbnail for ", filename, save_to, e.args)

from taghelpers import *
