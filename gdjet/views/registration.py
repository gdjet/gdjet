# -*- coding: utf-8 -*-
"""
    Registration Module for opt-in, double-opt-in etc.
"""

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotFound
from django.contrib.auth.models import User
from datetime import datetime

from gdjet import settings
from gdjet.models.registration import Registration
from gdjet.registration.override_this import post_registration, \
        post_validation, invalid_validation, RegistrationForm

from random import *
import string
from gdjet.registration.backends import get_backend
from django.shortcuts import redirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist

# all non-http_responses are consisting of the following tuple:
# (CODE, RequestContext object)
CODE_SUCCESS = 1
CODE_CLOSED = 2
CODE_SAME = 3 # same page (needs form corrections)
CODE_FAIL = 4 # the action has failed (may need form corrections)

def registration( request, 
                  template_name = "gdjet/registration/start.html", 
                  template_completed_name = "gdjet/registration/complete.html",
                  template_closed_name = 'gdjet/registration/closed.html',
                  post_registration_varname = 'reg',
                  # ^ registration object gets saved here on success 
                  http_response = True,
                  initial = None, # initial data for the form.
                  backend = None,
                  disallowed_url = 'gdjet_registration_closed',
                  form_class = None,
                  success_url = 'gdjet_registration_complete',
                  extra_context = None,
                   ):
    backend = get_backend(backend)
    CODE=CODE_SAME
    if not backend.registration_allowed(request):
        if not http_response:
            return (CODE_CLOSED, RequestContext(request))
        if disallowed_url:
            return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            r = form.cleaned_data
            r['email'] = r['regmail'] # clear the honeypot
            r['password1'] = r['password'] # be compatible, django-registration
            account = backend.register(request, **r)
            if not http_response:
                return (CODE_SUCCESS, RequestContext(request, 
                                      {post_registration_varname: r,
                                       'account': account 
                                       }))
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, 
                                                                      account)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
        else:
            CODE=CODE_FAIL
    else:
        form = form_class()
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request, {'form': form} )
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if http_response:
        return render_to_response(template_name,
                              context)
    else:
        return (CODE, context)


def validation( request, 
                template_name = "gdjet/registration/validation_start.html", 
                template_completed_name = 
                            "gdjet/registration/validation_success.html",
                template_fail_name = "gdjet/registration/validation.html",
                template_closed_name = 'gdjet/registration/closed.html',
                post_validation_varname = 'reg', # historic.
                http_response = True,
                backend = None,
                success_url=None, 
                extra_context=None, 
                **kwargs
                   ):
    backend = get_backend(backend)
    CODE=CODE_SAME # return code for non-http response.
    validation_code = None
    validation_user = None
    error = False
    error_already_active = False
    # gdjet does not use the direct activate approach natively
    # lookup if there is activation_key inside kwargs
    if ('activation_key' in kwargs.keys() and 
        settings.REGISTER_OPTIONS['direct_validation']):
        # this might be due to django-registration like usage.
        validation_code=kwargs['activation_key']
    else:
        if request.method=='GET' and 'a' in request.GET.keys():
            form = backend.get_validation_form_class(request)(request.GET)
            if form.is_valid():
                validation_code=form.cleaned_data['a']
                validation_user=User.objects.get(
                                            username=form.cleaned_data['u'])
            else:
                error = True
        elif request.method=='POST':
            form = backend.get_validation_form_class(request)(request.POST, 
                                                    files=request.FILES)
            if form.is_valid():
                validation_code=form.cleaned_data['a']
                validation_user=User.objects.get(
                                            username=form.cleaned_data['u'])
            else:
                error = True
    # activate if there is a validation form.
    if validation_code:
        # first get the registration object
        # we can also see if it is already validated here.
        reg=None
        if not settings.REGISTER_OPTIONS['direct_validation']:
            try:
                reg = backend.get_registration_object(validation_user, 
                                                      validation_code)
                if reg.validated: # actually, keys get deleted, so...
                    error_already_active=True
            except ObjectDoesNotExist:
                from gdjet.utils.log import log
                error = True # simple: this code is invalid after all.
                log('User tried to validate: %s, '\
                    'wrong validation code: %s' % (validation_user,
                                                    validation_code),
                    'gdjet.views.activate')
            except Exception, e:
                from gdjet.utils.log import log
                log('Validation got an Exception %s %s' % (e, e.message), 
                    'gdjet.views.activate')
                error = True
        if not error_already_active or error:
            # now get the account activated.
            account = backend.activate(request, 
                                       activation_key=validation_code,)
            if account:
                # success.
                if not http_response:
                    return CODE_SUCCESS, RequestContext(request,
                                        {'account': account,
                                         post_validation_varname: reg
                                         })
                if success_url is None:
                    to, args, kwargs = backend.post_activation_redirect(
                                                            request, account)
                    return redirect(to, *args, **kwargs)
                else:
                    return redirect(success_url)
            else:
                error = True
    # ALWAYS generate a new form.
    form = backend.get_validation_form_class(request)()
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request, {'form': form, 
                                       'error': error,
                                       'error_already_active': 
                                            error_already_active 
                                        })
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    if http_response:
        return HttpResponse( loader.get_template(template_name).render(context) )
    if error:
        CODE=CODE_FAIL
    return CODE, context

# django-registration compatibility functions:

def register(request, 
             backend, 
             success_url=None, 
             form_class=None,
             disallowed_url='registration_disallowed',
             template_name='registration/registration_form.html',
             extra_context=None,
             ):
    return registration(
                request,
                success_url=success_url,
                form_class=form_class,
                disallowed_url=disallowed_url,
                template_name=template_name,
                extra_context=extra_context,
                http_response=True
                        )

def activate(request, 
             backend,
             template_name='registration/activate.html',
             success_url=None, 
             extra_context=None, 
             **kwargs):
    return validation(request,
                      backend=backend,
                      template_name=template_name,
                      success_url=success_url,
                      extra_context=extra_context,
                      http_response=True,
                      **kwargs)
    