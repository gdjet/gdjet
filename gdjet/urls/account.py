# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('gdjet.views.account',
    url(r'^login', 'login', {}, name = 'gdjet_login' ),
    url(r'^logout', 'logout', {}, name = 'gdjet_logout' ),
    url(r'^welcome', 'welcome', {}, name = 'gdjet_welcome' ),
)
