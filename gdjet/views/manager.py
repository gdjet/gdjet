# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from gdjet import settings
from gdjet.models.manager import *
from gdjet import loader

def modules( request, basetemplate = 'gdjet/manager/base.html', 
             template = 'gdjet/manager/manager.html',
             message = "" ):
    t = loader.get_template( template )
    m = ManagerModule.objects.all()
    c = RequestContext(request,
    {
        'basetemplate': basetemplate, # use your own here.
        'message': message,
        'modules': m,
    })
    return HttpResponse( t.render(c) )

def amodule( request, name, template = 'gdjet/manager/amodule.html',
             message = "" ):
    t = loader.get_template( template )
    try:
        m = ManagerModule.objects.get( name__exact = name)
    except ManagerModule.DoesNotExist:
        message = "Module %s does not exist" % name
        m = None
    c = RequestContext(request, {
        'message': message,
        'modul': m,
    })
    return HttpResponse( t.render(c) )
