# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group

class Role( models.Model ):
    name = models.CharField( "Name", max_length = 50, unique = True )
    title = models.CharField("Titel", max_length = 200, default = "", blank = True )
    users = models.ManyToManyField( User, related_name = "roles", blank = True, null = True )
    groups = models.ManyToManyField( Group, related_name = "roles", blank = True, null = True )
    
    def add_user(self, user):
        self.users.add( user )
        self.save()
    
    def add_users(self, users = []):
        for user in users:
            self.users.add(user)
        self.save()
    
    def remove_user(self, user):
        try:
            self.users.remove(user)
            self.save()
        except:
            pass
    
    def add_group(self, group):
        self.groups.add( group )
        self.save()
    
    def has_user(self, user):
        try:
            self.users.get( id = user.id )
            return True
        except:
            return False
    
    class Meta:
        app_label = "gdjet"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
    
    