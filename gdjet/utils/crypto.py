# -*- coding: utf-8 -*-
'''

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

import hashlib

def md5_for_file(f, block_size=2**7,close_file=None):
    """
        reads a file block by block and applies md5 on it.
        you need a minimum block_size of 2**7 (128), 
        but you can use bigger ones as well.
        
        This is taken from Lars Wirzenius public snippet, 
        which is supposed to be public usage.
        http://stackoverflow.com/users/25148/lars-wirzenius
        
        modified to accept either a file object or a string.
        
        close_file: True (or anything true) always
                    False (never)
                    None (only if function opens it)
    """
    if isinstance(f, basestring):
        f=open(f, 'rb')
        close_file=True and (close_file or close_file is None)
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    if close_file:
        f.close()
    return md5.digest()