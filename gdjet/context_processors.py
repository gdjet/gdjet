# -*- coding: utf-8 -*-
"""
@author: g4b

Copyright (C) 2009 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from gdjet import settings

def often_used( request ):
    if request is not None:
        fullpath = request.get_full_path()
        host = request.get_host()
    else:
        fullpath = None
        host = None
    ret= {
        'MEDIA_URL': getattr( settings, "MEDIA_URL", ""),
        'STATIC_URL': getattr( settings, "STATIC_URL", ""),
        'PATH': getattr( request, "path", ""),
        'FULLPATH': fullpath,
        'HOST': host,
        'GET': getattr( request, "GET", ""),
        'META': getattr( request, "META", ""),
        'BASETEMPLATE': getattr( settings, "BASETEMPLATE", "base.html"),
        #'G4BTOOLS_PREFIX': getattr( settings, 'G4BTOOLS_PREFIX', '/gt/' ),
        #'G4BMANAGER_PREFIX': getattr( settings, 'G4BMANAGER_PREFIX', '/manager/' ),
        'PREFIX': getattr( settings, 'PREFIX', {} ),
        'STATIC': getattr(settings, 'STATIC', {}),
        'ADMIN_MEDIA_PREFIX': getattr(settings, 'ADMIN_MEDIA_PREFIX', '/media/'),
        }
    try:
        from gusr.models import UserProfile #@UnresolvedImport
        p = UserProfile.objects.get(user = request.user )
        ret['me'] = p
    except:
        pass
    return ret

def ninja(request):
    from gdjet.ninja.configbuilder import get_dojango_context
    return get_dojango_context(request)