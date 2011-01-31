# -*- coding: utf-8 -*-
'''

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''
from gdjet.forms.registration import RegistrationFormBase
from django.shortcuts import render_to_response
from django.template.context import RequestContext
"""
    Registration Module for Opt-In Registrations.
"""

from override_this import *

class Registration(object):
    """
        Controller Object for gdjet-registration.
    """
    def __init__(self,
                 templates={},
                 backend='gdjet.registration.backends.'\
                 'gdjet_registration.GdjetRegistrationBackend',
                 form_class=RegistrationFormBase,
                 ):
        tpl_std={
            'registration_start': 'gdjet/registration/start.html',
            'registration_complete': 'gdjet/registration/complete.html',
            'registration_closed': 'gdjet/registration/closed.html',
            'validation_start': 'gdjet/registration/validation.html',
            'validation_success': 'gdjet/registration/validation_success.html',
            'validation_error': 'gdjet/registration/validation.html',
                 }
        tpl_std.update(templates)
        self.templates=tpl_std
        self.form_class=form_class
        self.backend=backend
    
    def auto_urls(self, prefix='gdjet'):
        from django.conf.urls.defaults import include
        return (r'^%s' % self.base_url, include(self.urls(prefix)))
    
    def urls(self, prefix='gdjet'):
        from django.conf.urls.defaults import patterns, url
        return patterns( '',
            # validation/register functions
            url(r'^$', self.view_registration_start,
                { 'backend': self.backend,
                  'disallowed_url': '%s_registration_closed'%prefix,
                  'template_name': self.templates['registration_start'],
                  'success_url': '%s_registration_complete'%prefix,
                  # 'success': self.view_registration_complete,
                 },
                name='%s_registration_start' % ( prefix, )  ),
                
            url(r'^validate/$',
                self.view_validation_start,
                { 'backend': self.backend,
                  'disallowed_url': '%s_registration_closed'%prefix,
                  'template_name': self.templates['validation_start'],
                  'activation_key': None,
                  'success_url': '%s_validation_success'%prefix,
                 },
                name='%s_validation_start' % ( prefix, )  ),
            
            url(r'^validate/(?P<activation_key>\w+)$',
                self.view_validation_start,
                { 'backend': self.backend,
                  'disallowed_url': '%s_registration_closed'%prefix,
                  'template_name': self.templates['validation_start'],
                  'success_url': '%s_validation_success'%prefix,
                 },
                name='%s_validation_start' % ( prefix, )  ),
            
            # success/closed handlers:
            url('^complete/$',
                self.view_registration_complete,
                {'template': self.templates['registration_complete']},
                name='%s_registration_complete'%prefix,
                ),
            url(r'^validate/success/$',
               self.view_validation_success,
               {'template': self.templates['validation_success']},
                name='%s_validation_success' % prefix),
            url(r'^closed/$',
                self.view_registration_closed,
                {'template': self.templates['registration_closed']},
                name='%s_registration_closed' % prefix),
            
                        )
    
    # easy overwrite of that stuff:    
    def view_registration_start(self, request,
                                *args,
                                **kwargs):
        from gdjet.views.registration import register
        return register(request, *args, **kwargs )
    
    def view_registration_closed(self, request, template='gdjet/registration/closed.html'):
        return render_to_response(template,
                                  RequestContext(request)
                                  )
    
    def view_registration_complete(self, request, template='gdjet/registration/complete.html'):
        return render_to_response(template,
                                  RequestContext(request)
                                  )
    
    def view_validation_start(self, request,
                                *args,
                                **kwargs):
        from gdjet.views.registration import activate
        return activate(request, *args, **kwargs )
    
    def view_validation_success(self, request, template='gdjet/registration/validation_success.html'):
        return render_to_response(template,
                                  RequestContext(request)
                                  )
        
            

    