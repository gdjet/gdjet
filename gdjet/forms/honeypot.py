# -*- coding: utf-8 -*-
"""
    Honeypot Field and Widget for forms
    
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



# HoneypotFields are named as such to increase the chance that a bot
# will try to fill them in):
#
# class EmailForm(Form):
#    name = HoneypotField()
#    website = HoneypotField(initial='leave me')
#    email = EmailField()

from django import forms

EMPTY_VALUES = (None, '')

class HoneypotWidget(forms.TextInput):
    is_hidden = True
    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment
        super(HoneypotWidget, self).__init__(attrs, *args, **kwargs)
        if not self.attrs.has_key('class'):
            self.attrs['style'] = 'display:none'
    def render(self, *args, **kwargs):
        value = super(HoneypotWidget, self).render(*args, **kwargs)
        if self.html_comment:
            value = '<!-- %s -->' % value
        return value

class HoneypotField(forms.CharField):
    widget = HoneypotWidget
    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value
        raise forms.ValidationError('Anti-spam field changed in value.')
