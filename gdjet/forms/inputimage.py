# -*- coding: utf-8 -*-

from gdjet import settings
from django.forms import widgets
from gdjet.utils import get_aspect_ratio #@UnresolvedImport
from django.utils.safestring import mark_safe

class FileInputImageDisplay(widgets.FileInput):
    """
        Extends the file input widget by displaying an image over it.
    """
    max_width = None
    max_height = None
    def __init__(self, *args, **kwargs):
        if 'max_height' in kwargs:
            self.max_height = int(kwargs['max_height'])
            del kwargs['max_height']
        if 'max_width' in kwargs:
            self.max_width = int(kwargs['max_width'])
            del kwargs['max_width']
        widgets.FileInput.__init__(self, *args, **kwargs)
    def render(self, name, value, attrs=None):
        img = u'<!-- no image -->'
        if value:
            try:
                if not hasattr( value, 'width' ):
                    value.width = self.max_width
                if not hasattr( value, 'height'):
                    value.height = self.max_height
                width_string = ''
                height_string = ''
                if self.max_width or self.max_height:
                    width, height = get_aspect_ratio( value.width, value.height, self.max_width or value.width, self.max_height or value.height )
                    width_string = 'width="%spx" ' % width
                    height_string = 'height="%spx" ' % height
                img = u'<img src="' + value.url + '" %s%s><br />' % (width_string, height_string)
            except Exception, e:
                img = u'<!-- Error: %s -->' % e
        return mark_safe ( img + super(FileInputImageDisplay, self).render(name, None, attrs=attrs) )
