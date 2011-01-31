# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from gdjet import settings
from gdjet.urls import virtuals

urlpatterns = patterns('', )

if settings.MODULE_VIRTUALS and settings.MODULE_VIRTUALS_URLS:
    urlpatterns += virtuals.urlpatterns
