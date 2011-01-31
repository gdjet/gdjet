# -*- coding: utf-8 -*-
'''

Registration Backend Abstract Module

defines whatever function django-registration might need to work together
with gdjet. It is also used by gdjet internally.

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

class AbstractBackend(object):
    """ Override this and implement all functions to your needs """
    
    #also in django-registration
    def register(self, request, **kwargs):
        """
            returns the new user after registering.
        """
        pass
    
    #also in django-registration
    def activate(self, request, activation_key, **kwargs):
        """
            validation_code from gdjet is activation_key in registration.
            
        """
        pass
    
    def signal_user_activated(self, request, **kwargs):
        """
            sending the signal of an activated user via the
            django-registration way.
        """
        try:
            from registration import signals
        except ImportError:
            return False
        try:
            signals.user_activated.send( sender= self.__class__,
                                         user=kwargs['user'],
                                         request=request )
            return True
        except:
            return False
    
    #also in django-registration
    def registration_allowed(self, request, **kwargs):
        """
            tells you whether registration is even allowed.
            abstract defaults to false.
        """
        return False
    
    #also in django-registration
    def get_form_class(self, request):
        """
            return the form class for registration.
            abstract defaults to RegistrationFormBase
        """
        return RegistrationFormBase
    
    #also in django-registration
    def post_registration_redirect(self, request, user):
        """
            return the name of the url to redirect to after successfull
            user registration (django-registration)
        """
        pass
    
    #also in django-registration
    def post_activation_redirect(self, request, user):
        """
            return the name of the url to redirect to after successfull
            account activation (django-registration)
        """
        pass
