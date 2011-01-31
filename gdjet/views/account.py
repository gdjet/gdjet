# -*- coding: utf-8 -*-
from django.template.context import RequestContext
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from gdjet.forms.account import *
from django.contrib.auth import views as django_auth
from django.core.urlresolvers import reverse

def login( request, 
           next = '', 
           next_url = 'gdjet_welcome', 
           template = 'gdjet/account/login.html',
           template_name = None, # to be compatible with django.
           template_success = 'gdjet/account/login_success.html',
           template_inactive = 'gdjet/account/login_inactive.html'
           ):
    if template_name:
        template = template_name
    if 'next' in request.GET.keys():
        next = request.GET['next']
    if 'next_url' in request.GET.keys():
        next_url = request.GET['next_url']
    if 'next' in request.POST.keys():
        next = request.POST['next']
    if 'next_url' in request.POST.keys():
        next_url = request.POST['next_url']
    form = None
    if request.method == 'POST':
        form = LoginForm( request.POST )
        if form.is_valid():
            user = authenticate( username = form.cleaned_data['username'], 
                                 password = form.cleaned_data['password'],)
            if user is not None:
                if user.is_active:
                    django_auth.login(request, user)
                    # Redirect to a success page.
                    if next_url:
                        return HttpResponseRedirect( reverse( next_url ) )
                    if next:
                        return HttpResponseRedirect(next)
                    # or load the success loader.
                    return HttpResponse( loader.get_template( template_success ).render(
                                RequestContext(request, {}) ) )
                else:
                    # Return a 'inactive account' error message
                    c = RequestContext( request, {})
                    return HttpResponse( loader.get_template(template_inactive) )                    
        # Return an 'invalid login' error message.
        c = RequestContext( request, { 'form': form,
                                      'error': 'Invalid Login' })
    elif request.method == 'GET':
        form = LoginForm()
        c = RequestContext( request, {'form': form, 
                                      'next': next,
                                      'next_url': next_url })
    return HttpResponse( loader.get_template(template).render(c) )

def logout( request, next = None, next_url = None, 
            template = 'gdjet/account/logout.html',
            template_name = None ):
    if template_name:
        template = template_name
    if 'next' in request.GET.keys():
        next = request.GET['next']
    django_auth.logout(request)
    if next_url:
        return HttpResponseRedirect( reverse( next_url ) )
    if next:
        return HttpResponseRedirect(next)
    else:
        return HttpResponse( loader.get_template ( template ).render(
                                RequestContext(request, {}) ) )

def welcome( request, template = 'gdjet/account/welcome.html' ):
    if request.user.is_authenticated():
        c = RequestContext( request, {'user': request.user } )
        return HttpResponse( loader.get_template(template).render(c) )
    else:
        return login( request )