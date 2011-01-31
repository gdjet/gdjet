# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group, User

def register_permission(group, permission = None):
    if permission:
        group.permissions.add( permission )
        group.save()
        return group

# use this in management.py to create your groups.
def create_group( groupname, permissions = [], update = True ):
    group, created = Group.objects.get_or_create( name = groupname  )
    if created or update:
        if created:
            group.save()
        for permission in permissions:
            register_permission( group, permission )
        group.save()
    return group

# use this in applications only. or do it yourself over Groups :)
def get_group( groupname ):
    return Group.objects.get( name = groupname )

