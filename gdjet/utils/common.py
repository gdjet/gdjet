# -*- coding: utf-8 -*-

'''

Common Helper Functions

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

def ibool(something):
    other=False
    try:
        other=str(something).lower() in ['false', '0']
    except:
        pass
    return bool(something) and not other

def iget(something, variable, default=None):
    if isinstance(something, dict):
        return something.get(variable, default)
    else:
        try:
            return getattr(something, variable, default )
        except:
            return default

def build_list_including_callables( list_object, callable_args=None ):
    new_list = []
    for item in list_object:
        if callable(item):
            if callable_args:
                try:
                    item = item(**callable_args)
                except:
                    item = item()
            else:
                item = item()
        new_list += [ item ]
    return new_list

            