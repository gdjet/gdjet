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

import os

# We provide following imports relevant to filesystems:
from gdjet.utils.crypto import md5_for_file

def deltree(dirname):
    """
        Deletes a whole directory tree.
        This code is actually a public usage snippet and royalty free.
    """
    if os.path.exists(dirname):
        for root,dirs,files in os.walk(dirname):
            for dir in dirs:
                deltree(os.path.join(root,dir))
            for file in files:
                os.remove(os.path.join(root,file))     
        os.rmdir(dirname)