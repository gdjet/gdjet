# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('gdjet.views.virtuals',
    (r'^js/(?P<name>.*)\.js', 'show', { 'model_type': 'js' } ),
    (r'^js/(?P<name>.*)', 'show', { 'model_type': 'js' } ),
    (r'^css/(?P<name>.*)\.css', 'show', { 'model_type': 'css' } ),
    (r'^css/(?P<name>.*)', 'show', { 'model_type': 'css' } ),
    # (r'^redir/(?P<name>.*)', 'views.redir', ),
)