# -*- coding: utf-8 -*-

from django.forms import widgets
from gdjet import settings

DATE_FORMATS = [
'%d.%m.%Y', '%d.%m.%Y', '%d.%m.%y',
'%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
'%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
'%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
'%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
'%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'  
]


class CoolDateWidget(widgets.DateInput):
    format = '%d.%m.%Y'
    class Media:
        js = (
              settings.ADMIN_MEDIA_PREFIX + "js/core.js",
              settings.ADMIN_MEDIA_PREFIX + "js/calendar.js",
              settings.ADMIN_MEDIA_PREFIX + "js/admin/DateTimeShortcuts.js"
              )

    def __init__(self, attrs={}):
        super(CoolDateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'},
                                                format = self.format
                                                )