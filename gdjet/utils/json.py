# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json, datetime_safe
import datetime
import decimal
from time import mktime, struct_time
from django.utils.functional import Promise

class GdjetJSONEncoder( DjangoJSONEncoder ):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    
    g4b: enhanced to understand struct_time,
        and Promise objects
    @todo: file patch report, keep this one up to date.
    
    """
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, o):
        if isinstance(o, struct_time ):
            o = datetime.datetime.fromtimestamp(mktime(o))
            # we go on, super will do the rest.
        if isinstance(o, Promise):
            return unicode(o)
        else:
            return super(GdjetJSONEncoder, self).default(o)

class JSONDict( object ):
    """
        @author g4b
        Simple JSON diionary Object for Responses.
    """
    di = {}
    repr = ''
    
    def __init__(self, di = {}):
        if not self.di:
            self.di = di
        else:
            self.di.update( di )
    
    def dictify(self, di = {}):
        return simplejson.dumps( di, cls=GdjetJSONEncoder,)
    
    def out(self):
        if not self.repr:
            self.repr = self.dictify(self.di)
        return self.repr
    
    def __repr__(self):
        return self.out()
    
    def __unicode__(self):
        return u"%s" % self.out()
    
    def __str__(self):
        return self.out()
    
    def add(self, key, value):
        self.di[key] = value
        self.repr = self.dictify(self.di)
        return self
    
    def delete(self, key ):
        if key in self.di.keys():
            del self.di[key]
            self.repr = self.diify(self.di)
        return self
    
    def get(self, key, default = None ):
        if key in self.di.keys():
            return self.di[key]
        return default
    
class JSONResponse( HttpResponse ):
    status_code = 200
    default_content = ''
    default_dict = {}
    
    def update(self, content ):
        if isinstance( content, dict ):
            self.default_content.update( content )
        
    def __init__(self, content=None, verbose = False, **kwargs):
        
        if content is None:
            content = self.default_content
        elif isinstance( content, dict):
            c = {}
            c.update(self.default_dict)
            c.update(content)
            content = JSONDict(c).out()
        elif isinstance( content, JSONDict ):
            content = content.out()
        if verbose:
            print content
        HttpResponse.__init__( self, content, content_type = 'text/plain', **kwargs )

