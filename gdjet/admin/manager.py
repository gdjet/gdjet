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

from common import *
from gdjet.models.manager import *

class ManagerModuleOptionInline( admin.StackedInline ):
    model = ManagerOption
    allow_add = True
    extra = 0

class ManagerModuleStringInline( admin.StackedInline ):
    model = ManagerString
    allow_add = True
    extra = 0

class ManagerModuleTextInline( admin.StackedInline ):
    model = ManagerText
    allow_add = True
    extra = 0

class ManagerModuleUrlInline( admin.StackedInline ):
    model = ManagerUrl
    allow_add = True
    extra = 0

class ManagerModuleAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'label', 'description', 'enabled', 'restricted' )
    list_editable = ('enabled', 'restricted')
    list_filter = ('enabled', 'restricted')
    inlines = [ ManagerModuleOptionInline, ManagerModuleStringInline, ManagerModuleTextInline,
               ManagerModuleUrlInline ]
    
admin.site.register(ManagerModule, ManagerModuleAdmin)
