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
"""
    GDJET SETTINGS.
    Override some of the settings in your own settings file.
    
    Currently supported custom settings:
        STATIC_ROOT, STATIC_URL,
        LIVE_SERVER,
        STATIC, PREFIX, ROOTS,
        GDJET_MODULE_MANAGER, (False)
        GDJET_MODULE_VIRTUALS, (True)
        GDJET_MODULE_MONKEY, (is a dict)
        
        GDJET_MODULE_VIRTUALS_VTEMPLATES, (False)
        GDJET_REGISTER_START_ACTIVE (True) # no validation by default!
        GDJET_REGISTER_START_STAFF (False)
        GDJET_REGISTER_START_VALIDATED (True)
        GDJET_REGISTER_FROM_EMAIL (DEFAULT_FROM_EMAIL or mail@localhost - needed!)
        GDJET_CORRECT_OSLASH,
"""

from django.conf import settings
from functions import oneslash as oslash

MEDIA_ROOT = settings.MEDIA_ROOT
MEDIA_URL = settings.MEDIA_URL
DEBUG = settings.DEBUG
LANGUAGE_CODE = settings.LANGUAGE_CODE
ADMIN_MEDIA_PREFIX = getattr( settings, 'ADMIN_MEDIA_PREFIX', '/media/' )

# You can define Live Server as a variable to show, that this environment
# is a live server on the web. We assume true if not set.
# It is always used in conjuncture with DEBUG, but maybe you want
# a devel server to be "LIVE" and still on DEBUG...
LIVE_SERVER = getattr(settings, 'LIVE_SERVER', True)

# STATIC ROOT and URL define a separate folder for AppMedia.
# this means, you can symlink to application medias in /static/
# while holding dynamic media in MEDIA_URL
# set it to your applications directory if uncertain.
STATIC_ROOT = getattr(settings, 'STATIC_ROOT', settings.MEDIA_ROOT )
# set it to the directory where app-medias are symlinked.
STATIC_URL = getattr(settings, 'STATIC_URL', settings.MEDIA_URL )

# Prefix stores url-path-prefixes for g-apps. You can add your own, too
# Makes it easy to reference in templates: {{ PREFIX.GDJET }}/do_action.
PREFIX = getattr(settings, 'PREFIX', { 'GDJET': '/gdjet/' } )

# ROOTS stores STATIC_ROOT for application media.
# It's not really important d'oh. since it may not be used anyway anywhere.
ROOTS = getattr(settings, 'ROOTS', { 'GDJET': STATIC_ROOT + '/gdjet/media/' } )

# MEDIA files by applications are static media files, 
# you can use in tpl: {{ STATICS.GDJET }}images/something.jpg
STATIC = getattr( settings, 'STATIC', {
                                'JSLIB': STATIC_URL + '/ǵdjet/jslibs/',
                                'GDJET': STATIC_URL + '/gdjet/',
                                  } )

# Load overrides for this Toolset. You can control behaviour in your settings.py
MODULE_MANAGER = getattr( settings, 'GDJET_MODULE_MANAGER', False )
MODULE_TEST = getattr( settings, 'GDJET_MODULE_TEST', False )

MODULE_ADMINLOG = getattr( settings, 'GDJET_MODULE_ADMINLOG', True )

MODULE_REGISTRATION = getattr(settings, 'GDJET_MODULE_REGISTRATION', True )

MODULE_VIRTUALS = getattr(settings, 'GDJET_MODULE_VIRTUALS', True )

# disable database template loading by default (no speed down)
MODULE_VIRTUALS_VTEMPLATES = getattr( settings, 'GDJET_MODULE_VIRTUALS_VTEMPLATES', False )
# enable urlhandler for this module.
MODULE_VIRTUALS_URLS = getattr( settings, 'GDJET_MODULE_VIRTUALS_URLS', True )

# Email Handling
MODULE_MAILER = getattr( settings, 'GDJET_MODULE_MAILER', False )

MAILER_SKIP_MAILING = getattr( settings, 'GDJET_MAILER_SKIP_MAILING', False )
# Roles
MODULE_ROLES = getattr(settings, 'GDJET_MODULE_ROLES', False )

# Monkeypatching.
MODULE_MONKEY = getattr( settings, 'GDJET_MODULE_MONKEY', {
                                                'filebrowser_scale_and_crop': False,
                                                'filebrowser_convert_filename': False,
                                                           } )

PAGINATOR_STANDARD_TEMPLATE = getattr(settings, 'GDJET_PAGINATOR_STANDARD_TEMPLATE', None )


REGISTER_OPTIONS = {
        'username_min_length': 2, 
        'password_min_length': 6,
        # can be a callable returning a string
        'allowed_chars': 'abcdefghijklmnopqrstuvwxyz_.@+1234567890', # for username
        # a list of passwords not to be used.
        # can be a list of callables.
        'password_fail_list': [ 'geheim' , 'passwort' , 'password', 'asdfasdf' ],
        'mail_register': True, # mail a validation code. You want this.
        'mail_validated': False, # mail after validation occured.
        'direct_validation': False, # generate possibility for /validate/KEY urls?
        # note: gdjet uses GET variables, or a POST form.
        # django-registration allows direct links.
        # the url itself will work nevertheless.
                            }
REGISTER_OPTIONS.update(getattr(settings, 'GDJET_REGISTER_OPTIONS', {}))

# setting this to true would mean, all registering users are instantly registered.
REGISTER_START_VALIDATED = getattr( settings, 'GDJET_REGISTER_START_VALIDATED', False )
# setting this to true, the is_staff bit is set on new users, making admin apps possible.
REGISTER_START_STAFF = getattr( settings, 'GDJET_REGISTER_START_STAFF', False )
# all users validated are marked active. you really want this :)
REGISTER_START_ACTIVE = getattr( settings, 'GDJET_REGISTER_START_ACTIVE', True )
# the mail adress which sends the registration email.
REGISTER_FROM_EMAIL = getattr( settings, 'GDJET_REGISTER_FROM_EMAIL', 
                            getattr( settings, 'DEFAULT_FROM_EMAIL', 'mail@localhost' )
                            ) # please ensure you have this.
REGISTER_EXPIRATIONDELTA = getattr(settings, 'GDJET_REGISTER_EXPIRATIONDELTA',
                                   {'days': 30 }) # @see timedelta. 
                            #set to None if you do not want expirations.
REGISTER_OPEN = getattr(settings, 'GDJET_REGISTER_OPEN', False)


# Last bit: we correct urls/paths.
CORRECT_OSLASH = getattr(settings, 'GDJET_CORRECT_OSLASH', True)
# correct oneslashes:
if CORRECT_OSLASH:
    # correct oslash in PREFIX, ROOTS, STATIC
    for key in ROOTS.keys():
        ROOTS[key] = oslash( ROOTS[key] )
    for key in STATIC.keys():
        STATIC[key] = oslash( STATIC[key] )
    for key in PREFIX.keys():
        PREFIX[key] = oslash( PREFIX[key] )
    STATIC_URL = oslash( STATIC_URL )
    STATIC_ROOT = oslash( STATIC_ROOT )
    MEDIA_ROOT = oslash( MEDIA_ROOT )
    MEDIA_URL = oslash( MEDIA_URL )
