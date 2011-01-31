# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django import forms
from django.forms import widgets

from datetime import datetime

class ModelAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        # access self.fields here.

class ModelAdmin(admin.ModelAdmin):
    list_display = ( 'pk', )
    list_filter = ()
    list_editable = ()
    ## searching in model.
    search_fields = []
    search_fields_verbose = []
    ## use this form in admin.
    # form = ModelAdminForm
    ## define inlines here.
    # inlines = []
    ## fieldsets compatible to grappelli
    fieldsets = (
        ('Set1', {
            'classes': ('collapse open',),
            'fields': (),
        }),
        ('Set2', {
            'classes': ('collapse closed',),
            'fields': (),
        }),
        )
    
    def save_model(self, request, obj, form, change):
        # override this if you want to change a model on a save.
        obj.save()
    
    def queryset(self, request):
        # this query is displayed in the model admin index.
        qs = admin.ModelAdmin.queryset(self, request)
        return qs.all()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # change the formfield for some field here.
        # identify by db_field.name, change kwargs["queryset"],
        # return db_field.formfield(**kwargs)
        return admin.ModelAdmin.formfield_for_foreignkey(self, db_field, request, **kwargs)
    
    # ACTIONS
    actions = ['action_some']
    
    def action_some(self, request, queryset):
        pass
    action_some.short_description = "Some Description"
    
    # MEDIA
    class Media:
        js = []
        css = []
    