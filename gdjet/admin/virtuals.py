# -*- coding: utf-8 -*-
from gdjet.models.virtuals import Vcss, Vjs, Vtemplate
from common import *

class VcssAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vcss, VcssAdmin)

class VjsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vjs, VjsAdmin)

class VtemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Vtemplate, VtemplateAdmin)

