# -*- coding: utf-8 -*-
'''

    1. Either define PROJECT_ROOT in your project, or build your Project
    according to the gdjet deployment standard.
    
    2. define STATIC_SYMLINKS in your settings to deploy correctly.
    
    e.g.:
    STATIC_SYMLINKS = [
     ('%(APPS)s/filebrowser/media/filebrowser', '%(STATIC)s/filebrowser'),
     ('%(APPS)s/grappelli/media',   '%(STATIC)s/grappelli'),
     ('%(APPS)s/grappelli/media',   '%(STATIC)s/admin'),
            ]

    This command may become obsolete if Django handles this stuff itself
    (many things planned for Django 1.3)

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''
from django.db.models.loading import cache
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os

THIS_DIR = os.path.abspath( os.path.dirname(
            os.path.join( os.getcwd(), __file__ )) )

def deploy_static_symlinks( symlinks = [], SETTINGS = {} ):
    for source, dest in symlinks:
        if os.path.exists( dest % SETTINGS ):
            os.unlink( dest % SETTINGS )
            print "Removed %s" % os.path.abspath( dest % SETTINGS )
        os.symlink( source % SETTINGS, dest % SETTINGS )
        print "linking %s -> %s" % ( os.path.abspath( dest % SETTINGS), 
                                     os.path.abspath( source % SETTINGS ))

class Command(BaseCommand):
    help = ('Deploys paths according to settings, if its a gdjet project.',
            'Optional argument is the project path',
            'Define following in settings:',
        'PROJECT_ROOT if you want to have a certain directory to be the root',
        'STATIC_SYMLINKS which is a list of tuples, going through following:',
        'a dictionary with entries is given to be substituted:',
        ' PROJECT_ROOT with PROOT(=PROJECT_ROOT)',
        ' STATIC=PROOT+static,APPS=PROOT+applications,PROJ=PROOT+project',
        ' GRAPPELLI=grappelli path if grappelli is installed.',
        ' Example:',
        '  STATIC_SYMLINKS=[(\'%(GRAPPELLI)s/media\', \'%(STATIC)s/grappelli\')]'
            )
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        from django.conf import settings
        if len(args)>0:
            MY_DIR=args[0]
        elif getattr(settings, 'PROJECT_ROOT', None):
            MY_DIR=getattr(settings, 'PROJECT_ROOT')
        else:
            MY_DIR = os.path.join( THIS_DIR, '../../../..' )
        # @todo: make this editable via settings.
        SETTINGS = {
                    'STATIC': '%s/static' % MY_DIR,
                    'APPS': '%s/applications' % MY_DIR,
                    'PROJ': '%s/project' % MY_DIR,
                    #
                    'PROJECT_ROOT': MY_DIR,
            }
        
        # grappelli add-on: @todo: common importing of a list of names
        try:
            import grappelli
            gpath=os.path.abspath( os.path.dirname(
                            os.path.join( os.getcwd(), grappelli.__file__ )) )
            SETTINGS['GRAPPELLI']=gpath
        except ImportError:
            pass
        
        SYMLINKS = getattr( settings, 'STATIC_SYMLINKS', [] )
        print "Project Path is %s" % os.path.abspath( MY_DIR )
        print "Deploying Project Symlinks."
        deploy_static_symlinks(SYMLINKS, SETTINGS)
