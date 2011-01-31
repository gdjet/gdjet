# -*- coding: utf-8 -*-
'''
Gdjet Registration:
    After using it in some projects
    and stumbling over django-registration
    (which is a great app, you can find it at http://bitbucket.org/ubernostrum/django-registration)
    I extended the functionality to be very similar to django-registration
    
    Main differences:
        * You can inherit the Classes easily to create your own mechanics
        of calculating activation codes.
        * You can still use gdjet.registration as it was before.(1)
        * I use the Mail Queue built in in gdjet instead of django mail.

(1) Except if models have changed, which they sometimes did.

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

import random
import re
from datetime import datetime, timedelta

from django.db import models, transaction
from django.utils.hashcompat import sha_constructor
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from gdjet import settings
from gdjet.models.fields import JSONField

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class RegistrationManager(models.Manager):
    """
        Manages registrations.
        Mainly wrote it to be compatible with django-registration
        
    """
    def create_user(self, username, email, password, site=None, send_email=True,
                    active=settings.REGISTER_START_ACTIVE, 
                    staff=settings.REGISTER_START_STAFF, 
                    administrator=False,
                    first_name='', last_name='',
                    create_profile = False, # for django-registration... 
                    ):
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = active
        new_user.is_staff = staff
        new_user.is_administrator = administrator
        new_user.first_name=first_name
        new_user.last_name=last_name
        new_user.save()
        if create_profile:
            registration_profile = self.create_profile(new_user)
            if send_email:
                registration_profile.send_activation_email(site)
        return new_user
    create_user = transaction.commit_on_success(create_user)
    
    def create_inactive_user(self, username, email, password, site=None):
        # Actually does not do exactly, what it says.
        # it does not create an INACTIVE user, if global settings are different.
        # use directly create_user for this.
        # to be compatible with django-registration.
        return self.create_user(username, email, password, site, create_profile=True )
    
    def create_profile(self, user):
        # this is rather stupid in django-registration, but whatever.
        # gdjet provides the request object throughout.
        # normally the backend should do this in a separate step!
        return self.create_registration(None, user)
    
    def create_registration(self, request, user):
        """
            creates a registration object saving meta information
        """
        code=self.create_activation_hash(user.username)
        if request:
            # only in gdjet
            # we save stuff here
            register_ip = request.META.get('REMOTE_ADDR', '')
            register_data = request.META.get('HTTP_USER_AGENT', '')
        else:
            register_ip, register_data = '', ''
        r=self.create(user=user,
                      username=user.username,
                      validation_code=code,
                      register_ip=register_ip,
                      register_data=register_data)
        return r
    
    def activate_user(self, validation_code):
        """
            activates a user with a validation_code.
        """
        if self.validate_activation_hash(validation_code):
            try:
                reg = self.get(validation_code=validation_code)
            except ObjectDoesNotExist:
                return False
            if not reg.validation_code_expired():
                user = reg.user
                if not user:
                    return False
                user.is_active=True
                user.save()
                reg.validated=True
                reg.validation_code = None
                if not isinstance( reg.additional_data, dict ):
                    reg.additional_data = {}                    
                reg.additional_data['validation_date'] = datetime.now()
                reg.save()
                return user
        return False     
        
    def validate_activation_hash(self, hash, **kwargs):
        """
            validates an activation hash, if its valid.
        """
        if SHA1_RE.search(hash):
            return True
        return False
    
    def create_activation_hash(self, username, **kwargs ):
        """
            creates a valid activation hash.
            usually it works with username only.
            however if you define validate_activation_hash yourself
            you might add your own data to be hashed in.
        """
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        return sha_constructor(salt+username).hexdigest()
    
    def delete_expired_users(self, delete_registrations = False ):
        """
            deletes all non-active users who did not validate themselves.
            note: does not work if you have no expiration delta.
        """
        for reg in self.all():
            if reg.validation_code_expired():
                user = reg.user
                if user and not user.is_active:
                    if not delete_registrations:
                        reg.user = None
                        reg.validation_code = None
                        reg.save()
                    else:
                        reg.delete()
                    user.delete()
    
    def delete_expired_registrations(self):
        """
            deletes all expired registration objects, who do not have
            an associated user.
        """
        for reg in self.filter(user__isnull=True):
            if reg.validation_code_expired():
                reg.delete()
        

class Registration(models.Model ):
    """
        Registration object saves data about your key.
    """
    register_date = models.DateTimeField( editable = False, default = datetime.now )
    register_ip = models.IPAddressField( editable = False, default = "", blank = True, null = True )
    register_data = models.TextField( editable = False )
    
    validated = models.BooleanField( default = False ) # set to False if validation is programmed.
    validation_code = models.CharField( u"Validation Code", max_length = 100, blank=True, null=True)
    
    username = models.CharField(u"Username", max_length = 100, )
    user = models.ForeignKey( User, null=True, related_name='gdjet_registrations' )
    
    additional_data = JSONField( blank=True, null=True )
    objects = RegistrationManager()
    
    class Meta:
        app_label = 'gdjet'
        verbose_name = _("Registration")
        verbose_name_plural = _("Registrations")
    
    def activation_key_expired(self):
        """
            to be compatible with django-registration
        """
        return self.validation_code_expired()
    
    def validation_code_expired(self):
        """
            * checks if it is validated (in this case, its True)
            * checks if REGISTER_EXPIRATIONDELTA has been surpassed
            in which case it also may be True.
        """
        if self.validated: # no need for further investigation.
            return True
        # 
        delta = getattr(settings, 'REGISTER_EXPIRATIONDELTA', None )
        if not delta:
            return False # accounts cant expire.
        try:
            expiration_delta = timedelta( **delta )
        except:
            raise Exception( "GDJET:REGISTER_EXPIRATIONDELTA has wrong arguments." )
        return (self.register_date + expiration_delta <= datetime.now() )
    
    def send_activation_email(self, site):
        """
            This would send a mail.
            However it is only to be compatible with django-registration.
            for now.
        """
        pass