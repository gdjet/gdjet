# -*- coding: utf-8 -*-

'''

GDJET Registration Backend
usable with django-registration or gdjet internal registration.

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

from gdjet.registration.backends import abstract
from gdjet import settings
from gdjet.forms.registration import RegistrationFormBase, ValidationFormBase
from gdjet.models.registration import Registration
from gdjet.registration.email import send_mail
from django.contrib.sites.models import Site, RequestSite

class GdjetRegistrationBackend(abstract.AbstractBackend):
    
    def registration_allowed(self, request):
        return settings.REGISTER_OPEN
    
    def get_form_class(self, request):
        return RegistrationFormBase
    
    def get_validation_form_class(self, request=None):
        return ValidationFormBase
    
    def register(self, request, **kwargs):
        """
            returns the new user after registering.
        """
        username, email = kwargs['username'], kwargs['email']
        if 'password' in kwargs.keys():
            password = kwargs['password']
        else:
            password = kwargs['password1']
        try:
            if Site._meta.installed: #@UndefinedVariable
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
        except:
            site = None
        new_user = Registration.objects.create_user(username, email, password)
        regobj = Registration.objects.create_registration(request, new_user)
        if settings.REGISTER_OPTIONS.get('mail_register', True):
            # send the validation mail
            send_mail(new_user, 
                      regobj.validation_code, 
                      site, 
                      mail_text_template_file=kwargs.get('mail_text_template_file',
                                                'gdjet/registration/mail.txt'), 
                      mail_html_template_file=kwargs.get('mail_html_template_file',
                                                'gdjet/registration/mail.html'), 
                      subject=kwargs.get('subject',
                                        'Your Activation Code'), 
                      )
        return new_user
    
    def activate(self, request, activation_key=None):
        activated = Registration.objects.activate_user(activation_key)
        if settings.REGISTER_OPTIONS.get('mail_validated', True):
            # send the welcome mail
            pass
        return activated
    
    def get_registration_object(self, user, validation_code ):
        try:
            Registration.objects.get( user = user,
                                     validation_code = validation_code )
        except Registration.DoesNotExist:
            return Registration.objects.get(user=user)
    
    def post_registration_redirect(self, request, user,):
        return "gdjet_registration_complete", [], { 'user': user }
    
    def post_activation_redirect(self, request, user,):
        return "gdjet_validation_success", [], { 'user': user }
    
