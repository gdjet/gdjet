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

from django.forms import *
from gdjet.forms.fields import HoneypotField
from django.contrib.auth.models import User
from gdjet import settings
from gdjet.common import _
from gdjet.utils.common import iget, build_list_including_callables

USERNAME_MIN=iget( settings.REGISTER_OPTIONS, 'username_min_length', 2)
PASSWORD_MIN=iget( settings.REGISTER_OPTIONS, 'password_min_length', 6)

class RegistrationFormAbstract( forms.Form ):
    # no first/last name but with honeypot... well :)
    username = CharField( label=_("username"), 
                          max_length = 30,
                          min_length = USERNAME_MIN, 
                          help_text = _(u"Minimal length is %s")%USERNAME_MIN,
                          )
    regmail = EmailField( label = _("e-mail address"), )
    email = HoneypotField( _("e-mail address"), 
                           help_text = _('Do not enter anything here.') )
    password = CharField( label = _("password"), 
                          max_length = 100, 
                          min_length = PASSWORD_MIN, 
                          widget = widgets.PasswordInput(render_value=False),
                          help_text = _(u"Minimal length is %s")%PASSWORD_MIN,
                          )
    password_repeat = CharField( label = _("password repeat"), 
                          max_length = 100, 
                          min_length = PASSWORD_MIN, 
                          widget = widgets.PasswordInput(render_value=False),
                          help_text = _(u"Minimal length is %s")%PASSWORD_MIN,
                          )
    
    def clean_password_repeat(self):
        pw_fail_list = settings.REGISTER_OPTIONS['password_fail_list']
        if isinstance( pw_fail_list, basestring):
            # for backwards compatibility, blacklist can be CSV.
            pw_fail_list=pw_fail_list.split(',')
        else:
            # we only need to resolve callables, if it is a list.
            pw_fail_list = build_list_including_callables(pw_fail_list)
        #if len(self.cleaned_data['password']) < PASSWORD_MIN:
        #    raise forms.ValidationError(_("Password too short"))
        p_r = self.cleaned_data.get('password_repeat')
        if (p_r in pw_fail_list ):
            raise forms.ValidationError(
                    _('The entered password is blacklisted.')
                )
        else:
            # get the real password.
            p = self.cleaned_data.get('password', None)
            if p_r != p and p:
                raise forms.ValidationError(_('Passwords must match'))
            return p_r
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if username is None:
            raise forms.ValidationError(_('You have to define a username'))
        if len(username) < USERNAME_MIN:
            raise forms.ValidationError(_('Username too short. '\
                    'It must be at least %s characters long') % USERNAME_MIN)
        
        allowed_chars = iget(settings.REGISTER_OPTIONS, 'allowed_chars',
                             'abcdefghijklmnopqrstuvwxyz1234567890@.+-_')
        if callable(allowed_chars):
            allowed_chars=allowed_chars()
        for c in username:
            if c.lower() not in allowed_chars:
                raise forms.ValidationError(
                                _('Username containts unallowed characters'))
        try:
            u = User.objects.get( username__exact = username )
        except User.DoesNotExist: #@UndefinedVariable # stupid pydev.
            return username
        raise forms.ValidationError(_("Username already exists"))
    
    def clean_password(self):
        #if 'username' not in self.cleaned_data.keys():
        #    return ""
        pw_fail_list = settings.REGISTER_OPTIONS['password_fail_list']
        if isinstance( pw_fail_list, basestring):
            # for backwards compatibility, blacklist can be CSV.
            pw_fail_list=pw_fail_list.split(',')
        else:
            # we only need to resolve callables, if it is a list.
            pw_fail_list = build_list_including_callables(pw_fail_list)
        #if len(self.cleaned_data['password']) < PASSWORD_MIN:
        #    raise forms.ValidationError(_("Password too short"))
        if (self.cleaned_data['password'] in pw_fail_list ):
            raise forms.ValidationError(
                    _('The entered password is blacklisted.')
                                        )
        else:
            return self.cleaned_data['password']
    
class RegistrationFormBase( RegistrationFormAbstract ):
    first_name = CharField( label = _('first name'), max_length = 100 )
    last_name = CharField( label = _('last name'), max_length = 100 )

class ValidationFormBase( forms.Form ):
    u = CharField( label = _('username'), max_length = 30 )
    a = CharField( label = _('validation code'), 
                   max_length = 100,
                   min_length = 2 )
    
    def clean_u(self):
        try:
            u = User.objects.get( username__exact = self.cleaned_data['u'] )
        except User.DoesNotExist: #@UndefinedVariable # stupid pydev.
            raise forms.ValidationError(_("Invalid Data"))
        return u.username
    
    