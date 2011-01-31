# -*- coding: utf-8 -*-

"""
    Manager Models try to make you some application wide settings be available
    in the database.
    E.g.: You want a global setting, which is a string, save it with gdjet.manager
    This file represents the models used by gdjet.manager
"""

from django.db import models

class ManagerModule( models.Model ):
    name = models.CharField( u'Name', unique = True, max_length = 50, help_text = "Lowercase, no spaces!" )
    label = models.CharField( u'Label', max_length = 100 )
    icon = models.CharField( u'Icon', max_length = 100, blank = True, null = True )
    description = models.TextField( u'Description', blank = True, null = True)
    enabled = models.BooleanField( u'On/Off', default = True )
    restricted = models.BooleanField( u'Restricted', default = False )
    prefix = models.CharField( u'Prefix', max_length = 100, blank = True)
    
    def has_var(self, varname):
        # returns 1 if var exists, however
        # returns >1 if the variable exists in many categories.
        pass
    
    def get_var(self, varname ):
        # get variables in this order: option, string, text.
        # 
        pass
    
    def get_text(self, varname ):
        # gets a textvariable if its there.
        pass
    
    def get_string(self, varname ):
        # gets a string if its there.
        pass
    
    def get_option(self, varname):
        # gets an option( bool ) if there.
        pass
    
    def set_var(self, varname, value ):
        # sets in default order.
        # however, passing a string with a value if there is an option
        # will only save "True" in the option. be careful.
        pass
    
    def set_text(self, varname, value):
        # sets a variable by type text.
        pass
    
    def set_string(self, varname, value):
        pass
    
    def set_option(self, varname, value):
        pass
    
    def __unicode__(self):
        return "%s" % self.name
    
    class Meta:
        verbose_name = "ManagerModule"
        verbose_name_plural = "Manager Modules"
        app_label = 'gdjet'

class ManagerUrl( models.Model ):
    """
        an url. e.g. for functions.
        ignored by get_var.
    """
    module = models.ForeignKey( ManagerModule, related_name = 'urls' )
    name = models.CharField( u'Name', max_length = 50 )
    label = models.CharField( u'Label', max_length = 100 )
    sidebar = models.BooleanField( u'In Sidebar', default = False )
    icon = models.CharField( u'Icon', max_length = 100, blank = True, null = True )
    description = models.TextField( u'Description', blank = True, null = True)    
    url = models.CharField( u'URL', max_length = 254, default = '#' )
    
    def __unicode__(self):
        return "%s" % self.name
    
    class Meta:
        verbose_name = "ManagerURL"
        verbose_name_plural = "Manager URLs"
        app_label = 'gdjet'

class ManagerOption( models.Model ):
    """
        a boolean variable in the module.
    """
    module = models.ForeignKey( ManagerModule, related_name = 'options' )
    name = models.CharField( u'Name', max_length = 50 )
    label = models.CharField( u'Label', max_length = 100 )
    enabled = models.BooleanField( u'On/Off', default = False )
    
    def __unicode__(self):
        return "%s %s = %s" % ( self.module.name, self.name, self.enabled )
    
    class Meta:
        app_label = 'gdjet'

class ManagerString( models.Model ):
    """
        a string value.
    """
    module = models.ForeignKey( ManagerModule, related_name = 'strings' )
    name = models.CharField( u'Name', max_length = 50 )
    label = models.CharField( u'Label', max_length = 100 )
    value = models.CharField( u'Value', max_length = 254, blank = True,
                              default = '', null = True )
    
    def __unicode__(self):
        return "%s %s = %s" % ( self.module.name, self.name, self.value )
    
    class Meta:
        app_label = 'gdjet'

class ManagerText( models.Model ):
    """
        a text value, that is, big strings.
    """
    module = models.ForeignKey( ManagerModule, related_name = 'texts' )
    name = models.CharField( u'Name', max_length = 50 )
    label = models.CharField( u'Label', max_length = 100 )
    value = models.TextField( u'Value', blank = True, null = True )
    
    class Meta:
        app_label = 'gdjet'

# @todo: ManagerList
# @todo: managercomplex, saves and loads by php serialization. or json?
