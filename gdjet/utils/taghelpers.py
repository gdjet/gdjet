# -*- coding: utf-8 -*-

from django import template

def retrieve_value( var, context, default = None ):
    """
        retrieves the value in the context
        strings are stripped and returned stripped from their stringtags.
    """
    if var is None:
        return ''
    if '"' in var:
        real_var = var.strip('"')
        return real_var
    if "'" in var:
        real_var = var.strip("'")
        return real_var
    
    if '.' in var:
        try:
            r = template.Variable(var).resolve(context)
        except:
            try:
                r = template.Variable(".".join( var.split('.')[:-1] ) ).resolve( context )
                a = getattr( r, var.split('.')[-1], default )
                if not callable(a):
                    return a
                else:
                    return a()
            except Exception, e:
                # print "retrieve_value: Calling Function resulted in Error %s" % e
                raise Exception( "Variable not found in template context (and last part not callable): %s" % var )
    try:
        return template.Variable(var).resolve(context)
    except:
        if default:
            return default
        raise Exception("Variable not found in template context: %s" % var)
    
def retrieve_values( l, context, ignore_unfound = False ):
    """
        retrieves values in a list.
    """
    if isinstance(l, list):
        r = []
        for i in l:
            try:
                r += [ retrieve_value(i, context) ]
            except:
                if not ignore_unfound:
                    raise
        return r
    else:
        try:
            return retrieve_value(l, context)
        except:
            if not ignore_unfound:
                raise
            return ''