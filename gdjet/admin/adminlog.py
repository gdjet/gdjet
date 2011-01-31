# -*- coding: utf-8 -*-
from common import *
from gdjet.models.adminlog import AdminLog

class AdminLogAdmin(admin.ModelAdmin ):
    list_display = ( 'id', 'by', 'date', 'message', 'severity' )
    list_filter = ('severity', 'by')

admin.site.register(AdminLog, AdminLogAdmin )
    