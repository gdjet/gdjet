# -*- coding: utf-8 -*-
from django.contrib.admin import AdminSite
from django.conf.urls.defaults import patterns
from gdjet.views import manager as views

def create_manager_adminsite( Base = AdminSite ):
    class ManagerAdminSite( Base ):
        def get_urls( self  ):
            urls = super(ManagerAdminSite, self).get_urls( )
            my_urls = patterns('',
                (r'^manager/module/(?P<name>.*)', self.admin_view( views.amodule ) ),
                (r'^manager',   self.admin_view( views.modules) ),
                # (r'^my_view/$', self.admin_site.admin_view(  ))
            )
            return my_urls + urls
    return ManagerAdminSite
