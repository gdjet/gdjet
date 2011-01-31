# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
    Admin Classes for Registration

@author: g4b

LICENSE AND COPYRIGHT NOTICE:

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from gdjet.admin.common import *
from gdjet.models.registration import *

class RegistrationAdmin(admin.ModelAdmin ):
    list_display = ('username', 'validation_code', 'validated', 'register_date', 'register_ip',)

admin.site.register( Registration, RegistrationAdmin )