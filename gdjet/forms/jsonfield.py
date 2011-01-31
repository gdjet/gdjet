# -*- coding: utf-8 -*-
"""
    JSON Field and Widget for forms
    
    @author g4b
"""
'''

Copyright (C) 2009 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

from django import forms

class JSONListWidget( forms.TextInput ):
    pass

class JSONListField(forms.CharField):
    widget = forms.MultipleHiddenInput
    def clean(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return None
        if isinstance( value, basestring ):
            return [ value, ]
        raise forms.ValidationError('Value (%s) has unknown Type: %s' % (value, type(value)) )
