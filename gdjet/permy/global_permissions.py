# -*- coding: utf-8 -*-
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def register_application_permissions( appname, permissions ):
    ret = {}
    ct, created = ContentType.objects.get_or_create(model='', app_label=appname,
                                                        defaults={'name': appname})
    for codename, name in permissions:
            p, created = Permission.objects.get_or_create(codename=codename,
                            content_type__pk=ct.id,
                            defaults={'name': name, 'content_type': ct})
            ret[codename] = p
    return ret


def register_application_permission( appname, key, title ):
    return register_application_permissions( appname, (( key, title ),) )

