# -*- coding: utf-8 -*-

from common import *
from gdjet.models.roles import *

class RoleAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'title', )

admin.site.register(Role, RoleAdmin)