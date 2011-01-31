# -*- coding: utf-8 -*-
from gdjet import settings
from django.template import RequestContext, Template, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from gdjet.models.virtuals import *

def show( request, name, model_type = 'txt', response_type = None, render = True ):    
    if model_type == 'js':
        VModel = Vjs
        response_type = 'text/javascript'
    elif model_type == 'css':
        VModel = Vcss
        response_type = 'text/css'
    else:
        raise Exception("VModel of Type %s does not exist." % model_type )
    try:
        vm = VModel.objects.get( url = name.lower() )
        ret = vm.data
        t = Template( ret )
    except VModel.DoesNotExist:
        # we try to load the template.
        ret = u""
        t = loader.get_template("%s.%s" % ( name, model_type ) )
        
    if render:
        c = RequestContext( request, {
                'MEDIA_URL': settings.MEDIA_URL,
                'STATIC_URL': settings.STATIC_URL,
                'PATH': request.path,
                'FULLPATH': request.get_full_path(),
                'HOST': request.get_host(),
                'GET': request.GET,
                'META': request.META,
                      } )
        ret = t.render( c )
    return HttpResponse( ret, response_type )
    
