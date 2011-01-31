# -*- coding: utf-8 -*-
# This Template gives you a mostly used Admin Class
# It can define own views, which can be accessed via Actions.
# It does allow save_model, queryset, and formfields to be overwritten
# And it does show you, how Grappelli Fields are to be overwritten.
# 

# Useful imports:
from django.contrib import admin
from django.conf import settings
from django import forms
from django.forms import widgets
# from gblg.widgets import ModelMultipleChoiceFieldCheckboxes, CheckboxSelectMultipleIndent #@UnresolvedImport
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, RequestContext
from django.conf.urls.defaults import *

class Something():
    pass # Dummy, Something is of course your Model Class.
    # from models import * ;)

# 8< ---- Start Snip Here -- >8

class SomethingAdmin(admin.ModelAdmin):
    """
    """
    # Defaults:
    # list_display = ( 'pk', )
    # list_filter = ( , )
    # list_editable = ( , )
    # search_fields = []
    # search_fields_verbose = []
    # form = SomethingAdminForm
    # change_list_template = "admin_list.html"
    # change_form_template = "admin_change.html"
    # inlines = []
    # fieldsets = (
    #    ('Main', {
    #        'classes': ('collapse open',), # collapse-open is deprecated.
    #        'fields': ( 'pk'),
    #    }),
    #    )
    
    # Important functions:
    def save_model(self, request, obj, form, change):
        obj.save()
    
    def queryset(self, request):
        """ default queryset
        """
        qs = admin.ModelAdmin.queryset(self, request)
        return qs.all().order_by( 'pk' )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #if db_field.name == "thread":
        #    kwargs["queryset"] = ArtikelGruppe.objects.filter(owner=request.user)
        #    return db_field.formfield(**kwargs)
        return admin.ModelAdmin.formfield_for_foreignkey(self, db_field, request, **kwargs)
        
    # Custom VIEWS
    def view_something(self, request, ids):
        items = None
        if ids == 'all':
            items = Something.objects.all()
        else:
            pks = ids.split(',')
            items = Something.objects.filter(  pk__in = pks )
        # return HttpResponse()
        
    def get_urls(self):
        """
            custom urls.            
        """
        urls = admin.ModelAdmin.get_urls(self)
        my_urls = patterns('',
            (r'^something/(?P<ids>.+)/$', self.admin_site.admin_view( self.view_something ) ),
        )
        # return my_urls + urls # make sure my_urls is BEFORE standard urls!
        return urls
    
    # Custom Actions
    actions = []
    
    def get_actions(self, request):
        actions = admin.ModelAdmin.get_actions(self, request)
        # del actions['delete_selected'] # delete default delete action
        return actions
    
    def action_something(self, request, queryset ):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("something/" % ( ",".join(selected) ) )
    action_something.short_description = "Describe your Action here"
    
    class Media:
        pass
