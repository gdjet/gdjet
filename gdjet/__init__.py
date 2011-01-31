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

"""
    GDJET - - - g4b's DJANGO TOOLSET
    This Application should unite g4bmanager and g4butils to a new
    and better baseproject, offering various helpful systems for django
    applications.
    Basic Plans:
        - gdjet.manager: adds the ability to save module settings
                    in the database. helpful functions should help
                    you to save and retrieve project settings.
        - gdjet.forms: Adds helpful forms, fields, and widgets, example
                    giving: honeypot, timepot, etc.
        - gdjet.monkey: Monkeypatcher module for patching various functions
    
    Best usage: use grappelli, django-filebrowser, dojango, south together
        with gdjet.
"""

VERSION=(1,0,1)