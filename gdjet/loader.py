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

"""
    this templateloader only seeks the database if both:
    MODULE_VIRTUALS AND MODULE_VIRTUALS_VTEMPLATES are enabled!
"""

# Custom Template Loader Hack.
# (C) by Gabor Guzmics 2009-2010

from gdjet import settings
from django.template import Template, loader
from gdjet.models.virtuals import Vtemplate 

def get_template( template_name ):
    if not (settings.MODULE_VIRTUALS and settings.MODULE_VIRTUALS_VTEMPLATES):
        return loader.get_template( template_name )
    M = Vtemplate # for pydevs stupidity
    try:
        tobj = M.objects.get( url = template_name )
        return Template(tobj.data)
    except M.DoesNotExist:
        return loader.get_template( template_name )
    