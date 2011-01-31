# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from gdjet.utils import retrieve_value
import re

register = template.Library()

class PercentNode(template.Node):
    def __init__(self, var_name = None, var_value = None, var_newvar = None,
                 raw = False ):
        self.var_name = var_name
        self.var_value = var_value
        self.var_newvar = var_newvar
        self.raw = raw
    def render(self, context):
        if not self.var_name:
            return ''
        try:
            sum = float( retrieve_value( self.var_name, context)  )
        except:
            raise
        try:
            percent = int( retrieve_value ( self.var_value, context ) )
        except:
            raise
        psum = ( sum * percent / 100.0 )
        
        if not self.raw:
            sum = sum + psum
        else:
            sum = psum
        
        if self.var_newvar:
            context[self.var_newvar] = sum 
        else:
            return sum
        return ''

@register.tag
def adjust_by_percent(parser, token):
    """
        Adjusts a Field by Percent
        {% adjust_by_percent something percent [as var] %}
    """
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(\S+) (\S+) as (\S+)', arg)
    if not m:
        m = re.search(r'(\S+) (\S+)', arg)
        if not m:        
            raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
        var_name, var_value = m.groups()
        return PercentNode(var_name, var_value)
    var_name, var_value, var_newvar = m.groups()
    return PercentNode(var_name, var_value, var_newvar)

@register.tag
def percent_from(parser, token):
    """
        Gets a Percentage from Sth.
        {% percent_from something percent [as var] %}
    """
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(\S+) (\S+) as (\S+)', arg)
    if not m:
        m = re.search(r'(\S+) (\S+)', arg)
        if not m:        
            raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
        var_name, var_value = m.groups()
        return PercentNode(var_name, var_value, raw = True )
    var_name, var_value, var_newvar = m.groups()
    return PercentNode(var_name, var_value, var_newvar, raw = True )

@register.filter
@stringfilter
def divide(value, divisor):
    try:
        return int( int(value) / float(divisor) )
    except:
        return ''

@register.filter
@stringfilter
def multiply(value, multiplicator):
    try:
        return int( int(value) * int(multiplicator) )
    except:
        return ''

@register.filter
@stringfilter
def as_int(value):
    try:
        return int(value)
    except:
        return ''

