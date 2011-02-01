# -*- coding: utf-8 -*-
'''

This classes can be used to create a template context variable
which returns paths. Very useful if you want to dynamically import templates.
Create a TPL Variable, holding one or several PathAttribute objects
each defining it's own prefixes

Copyright (C) 2010 by  Gabor Guzmics, <gab(at)g4b(dot)org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

class BasicTPLHelper(object):
    def html(self):
        return self.__unicode__()
    
    def __hasattr__(self, attribute):
        if attribute in ['render']:
            return False
        return True

class PathAttributeSpawn(BasicTPLHelper):
    """
        Spawned by the PathAttribute this class extends its own path
        at every getattr call.
    """
    def __init__(self, path, extension='html'):
        self.path=path
        self.extenstion=extension
        
    def __getattr__(self, key):
        self.path=u"%s/%s" % (self.path, key)
        return self
    
    def __unicode__(self):
        return u"%s.%s" % ( self.path, self.extension )
    
    def __repr__(self):
        return self.__unicode__()

class PathAttribute(BasicTPLHelper):
    """
        An object which can hold a certain prefix and returns a path
        if accessed via attributes.
        
        something=PathAttribute()
        something.directory.subdirectory.file
        will return:
        "directory/subdirectory/file.html"
        
        This class uses a spawn object for each call which after that
        keeps itself intact.
        
        If you need them to be individual, please use PathAttributeReplicator
        Note: the Replicator creates new instances at every getattr!
    """
    def __init__(self, path=None, extension='html', prefix='',):
        self.extension=extension
        if prefix and path:
            self.path=u"%s/%s" % (prefix, path)
        elif prefix:
            self.path=prefix
        else:
            self.path=path
            
    def __unicode__(self):
        return u"%s.%s" % ( self.path, self.extension )
    
    def __repr__(self):
        return self.__unicode__()
    
    def __getattr__(self, key):
        if not self.path:
            return PathAttributeSpawn( key, self.extension )
        return PathAttributeSpawn( u"%s/%s" % (self.path, key), self.extension )

class PathAttributeReplicator(BasicTPLHelper):
    """
        Most safe way to create pathattributes, since they create new
        objects at each getattr, which is however slower.
    """
    def __init__(self, path=None, extension='html', prefix='',):
        self.extension=extension
        if prefix and path:
            self.path=u"%s/%s" % (prefix, path)
        elif prefix:
            self.path=prefix
        else:
            self.path=path
    
    def __getattr__(self, key):
        if not self.path:
            return PathAttributeReplicator( key, self.extension )
        return PathAttributeReplicator( u"%s/%s" % (self.path, key), self.extension )
    
    def __unicode__(self):
        return u"%s.%s" % ( self.path, self.extension )
    
    def __repr__(self):
        return self.__unicode__()

    