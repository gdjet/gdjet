# -*- coding: utf-8 -*-

from gdjet.models.manager import *

def register_module( name, label, enabled = True, restricted = False, prefix = '',
                     description = 'This module has no description.',
                     icon = None ):
    try:
        m = ManagerModule.objects.get( name__exact = name )
    except ManagerModule.DoesNotExist:
        m = ManagerModule( 
                          name = name,
                          label = label,
                          enabled = enabled,
                          restricted = restricted,
                          prefix = prefix,
                          description = description,
                          icon = icon,
                           )
        m.save()
    return m

def register_url( mname, name, url, label = None, 
                       sidebar = True, description = None, icon = None ):
    try:
        m = ManagerModule.objects.get( name__exact = mname )
    except ManagerModule.DoesNotExist:
        return False
    try:
        mp = ManagerUrl.objects.get( name__exact = name )
    except:
        if not label:
            label = name
        mp = ManagerUrl( 
                        module = m,
                        name = name,
                        label = label,
                        sidebar = sidebar,
                        url = url,
                        description = description,
                        icon = icon,
                            )
        mp.save()
    return mp

def register_option( mname, name, label = None, enabled = False):
    try:
        m = ManagerModule.objects.get( name__exact = mname )
    except ManagerModule.DoesNotExist:
        return False
    try:
        mp = ManagerOption.objects.get( name__exact = name )
    except:
        if not label:
            label = name
        mp = ManagerOption( 
                        module = m,
                        name = name,
                        label = label,
                        enabled = enabled,
                            )
        mp.save()
    return mp

def register_string( mname, name, label = None, value = ''):
    try:
        m = ManagerModule.objects.get( name__exact = mname )
    except ManagerModule.DoesNotExist:
        return False
    try:
        mp = ManagerString.objects.get( name__exact = name )
    except:
        if not label:
            label = name
        mp = ManagerString( 
                        module = m,
                        name = name,
                        label = label,
                        value = value,
                            )
        mp.save()
    return mp

def get_option( mname, name ):
    try:
        option = ManagerOption.objects.get( module__name__exact = mname, name__exact = name )
        return option.enabled
    except ManagerOption.DoesNotExist:
        return None

def set_option( mname, name, enabled = None ):
    if enabled is None:
        return False
    elif isinstance(enabled, str):
        if (enabled == 'true') or (enabled == ''):
            enabled = True
        else:
            enabled = False
    try:
        option = ManagerOption.objects.get( module__name__exact = mname, name__exact = name )
        option.enabled = enabled
        option.save()
        return True
    except ManagerOption.DoesNotExist:
        return False


def get_string( mname, name, default_value = None ):
    try:
        option = ManagerString.objects.get( module__name__exact = mname, name__exact = name )
        return option.value
    except ManagerString.DoesNotExist:
        return default_value

def set_string( mname, name, value = None ):
    if value is None:
        return False
    try:
        option = ManagerString.objects.get( module__name__exact = mname, name__exact = name )
        option.value = value
        option.save()
        return True
    except ManagerString.DoesNotExist:
        return False

def get_text( mname, name, default_value = None ):
    try:
        option = ManagerText.objects.get( module__name__exact = mname, name__exact = name )
        return option.value
    except ManagerText.DoesNotExist:
        return default_value

def set_text( mname, name, value = None ):
    if value is None:
        return False
    try:
        option = ManagerText.objects.get( module__name__exact = mname, name__exact = name )
        option.value = value
        option.save()
        return True
    except ManagerText.DoesNotExist:
        return False
