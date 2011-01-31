# -*- coding: utf-8 -*-
from gdjet import settings

if settings.MODULE_VIRTUALS:
    from virtuals import *

if settings.MODULE_MANAGER:
    from manager import *

if settings.MODULE_REGISTRATION:
    from gdjet.registration.admin import *

if settings.MODULE_ADMINLOG:
    from adminlog import *

if settings.MODULE_MAILER:
    from mailer import *

if settings.MODULE_ROLES:
    from roles import *
