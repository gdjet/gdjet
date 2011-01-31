# -*- coding: utf-8 -*-
from gdjet.models.adminlog import AdminLog
from gdjet import settings

def log( message, by = 'gdjet.utils.log', severity = 10 ):
    if settings.MODULE_ADMINLOG:
        AdminLog( message = message,
                  by = by,
                  severity = severity ).save()
    else:
        print "LOG(%s): %s by %s" % ( severity, message, by )
    