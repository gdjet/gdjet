# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def permission( mdl, name ):
    """
        Retrieves the permission named name for mdl
    """
    if isinstance(mdl, str):
        # get the mdl from contenttype
        raise Exception("Not supported yet.")
    else:
        #@todo: look up if this is an instance!
        pass
    # now get the contenttype for this model.
    ct = ContentType.objects.get_for_model( mdl )
    # now get the permission named "name" for this model.
    try:
        p = Permission.objects.get(codename=name,
                            content_type__pk=ct.id,)
    except Permission.DoesNotExist, e: #@UndefinedVariable
        return None
    return p
    

def permission_add( mdl ):
    return permission( mdl, 'add_%s' % mdl.__name__.lower() )

def permission_change( mdl ):
    return permission( mdl, 'change_%s' % mdl.__name__.lower() )

def permission_delete( mdl ):
    return permission( mdl, 'delete_%s' % mdl.__name__.lower() )
