from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from gdjet.utils import retrieve_value
from gdjet.utils.intervals import number_intervals
import re
from gdjet.utils.strings import args_split_list
from gdjet.utils.taghelpers import retrieve_values
from gdjet.pagination.paginator import Pagination

register = template.Library()

class GetsNode(template.Node):
    def __init__(self, var_args = None, opts = ''):
        self.var_args = var_args
        self.opts = opts
        
    def render(self, context):
        # try to get "request"
        gets = None
        try:
            req = template.Variable("request").resolve(context)
            gets = req.GET
        except:
            try:
                gets = template.Variable("GET").resolve(context)
            except:
                raise
        
        args = args_split_list( self.var_args, single_no_list = True )
        
        
        real_gets = {}
        if gets and 'fresh' not in self.opts:
            for getkey in gets.keys():
                real_gets[str(getkey)] = gets[getkey]
        gets = real_gets
        
        for k in args.keys():
            if k.startswith('!'):
                if k[1:] in gets.keys():
                    del gets[k[1:]]
                continue
            elif k.startswith('?'):
                if k[1:] not in gets.keys():
                    continue
                gets[k[1:]] = retrieve_values( args[k], context, True )
            else:
                gets[ k ] = retrieve_values( args[k], context, True )
        
        # @todo URIENCODE.
        gets_str = ''
        for get in gets.keys():
            if not gets_str:
                if gets[get]:
                    gets_str = '?%s=%s' % (get, gets[get])
                else:
                    gets_str = '?%s=' % get
            else:
                if gets[get]:
                    gets_str += '&%s=%s' % (get, gets[get])
                else:
                    gets_str += '&%s=' % get
        if '?' in self.opts: 
            if gets_str == '':
                gets_str = '?'
            else:
                gets_str = gets_str + '&'
        if 'plain' in self.opts:
            if gets_str.startswith('?') or gets_str.startswith('&'):
                return gets_str[1:]
        return gets_str

@register.tag
def gets(parser, token):
    """
        used to retrieve the actual GET variables as ?var=value&var2=value
        
        syntax is:
            {% gets variable1='value1' variable2=contextvar %}
        
        you can delete variables with:
            !varname=
    """
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        return GetsNode()
    m = re.search(r'(.+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r could not parse its arguments %s" % (tag_name, arg)
    return GetsNode(m.group())

@register.tag
def gets_open(parser, token):
    """
        like gets, but leaves the GET line open (if no variables: ?, else: &)
        e.g. instead of
        ?a=b&c=d
        it returns
        ?a=b&c=d&
        and if no variables are found, it leaves the open ?
    """
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        return GetsNode()
    m = re.search(r'(.+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r could not parse its arguments %s" % (tag_name, arg)
    return GetsNode(m.group(), opts = '?')

@register.tag
def gets_js(parser, token):
    """
        used to retrieve the actual GET variables as ?var=value&var2=value
        
        syntax is:
            {% gets variable1='value1' variable2=contextvar %}
        
        you can delete variables with:
            !varname=
    """
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        return GetsNode()
    m = re.search(r'(.+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r could not parse its arguments %s" % (tag_name, arg)
    return GetsNode(m.group(), opts = ['plain'])

class SliceNode( template.Node ):
    def __init__(self, var_name = None, 
                    var_from = None, var_to = None, var_newname = None ):
        self.var_name = var_name
        self.var_from = var_from
        self.var_to = var_to
        self.var_newname = var_newname
    def render(self, context):
        if not self.var_name:
            return ''
        v = retrieve_value( self.var_name, context )
        to, fr = None, None
        if self.var_to:
            to = retrieve_value( self.var_to, context )
        if self.var_from:
            fr = retrieve_value ( self.var_from, context )
        
        if to is not None and fr is not None:
            s = v[fr:to]
        elif fr is not None:
            s = v[fr:]
        elif to is not None:
            s = v[:to]
        else:
            s = v[:]
        
        if self.var_newname:
            context[self.var_newname] = s
        else:
            context[self.var_name ] = s
        return ''
        
@register.tag
def slice(parser, token):
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(\S+) (\S+) as (\S+)', arg.strip())
    var_newname = None
    if not m:
        m = re.search(r'(\S+) (\S+)', arg.strip())
        var_name, slicing = m.groups()
        if not m:
            raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    else:
        var_name, slicing, var_newname = m.groups()
    try:
        var_from, var_to = slicing.split(':')
        #print "slicing: %s - %s" % (var_from, var_to)
    except:
        raise template.TemplateSyntaxError, "%r tag needs slicing argument (no : detected?)"
    return SliceNode(var_name, var_from, var_to, var_newname)

class VarNode(template.Node):
    def __init__(self, var_name = None, var_value = None):
        self.var_name = var_name
        self.var_value = var_value
    def render(self, context):
        if not self.var_name:
            return ''
        #if context.has_key(self.var_name):
        #    raise Exception( "context: %s" % context )        
        context[self.var_name] = retrieve_value ( self.var_value, context )
        return ''

@register.tag
def var(parser, token):
    """
        creates a new context variable with a value
        usage: {% var somekey is 'something' %}
        its not a block tag like "with".
        but you should use it in a with tag.
    """
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(\S+) is (.+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    var_name, var_value = m.groups()
    return VarNode(var_name, var_value)


class GetAttrNode(template.Node):
    def __init__(self, var_name = None, var_attr = None, var_new = None):
        self.var_name = var_name
        self.var_attr = var_attr
        self.var_new = var_new
    def render(self, context):
        if not self.var_name:
            return ''
        what = self.var_name
        attrname = retrieve_value ( self.var_attr, context )
        try:
            v = template.Variable("%s.%s" % (self.var_name, attrname) ).resolve(context)
            if callable(v):
                v = v()
            if self.var_new:
                context[self.var_new] = v 
            else:
                return template.Variable("%s.%s" % (what, attrname) ).resolve(context)
        except:
            raise Exception("%s %s %s" % (self.var_name, self.var_attr, self.var_new) )
        return ''

@register.tag
def getattr(parser, token):
    """
        gets the attribute of a variable.
    """
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(\S+) (\S+) as (.+)', arg)
    if not m:
        m = re.search(r'(\S+) (\S+)', arg.strip())
        if not m:        
            raise template.TemplateSyntaxError,\
                    "%r tag had invalid arguments" % tag_name
        var_name, var_attr = m.groups()
        return GetAttrNode(var_name, var_attr,)        
    var_name, var_attr, var_new = m.groups()
    return GetAttrNode(var_name, var_attr, var_new)

class IntervalNode(template.Node):
    def __init__(self, var_args = [], var_asname = [] ):
        self.var_args = var_args
        self.var_asname = var_asname
        
    def render(self, context):
        if not self.var_args or not self.var_asname:
            return ''
        if isinstance( self.var_args, list ):
            args =[]
            for attr in self.var_args:
                num = retrieve_value ( attr, context, 0 )
                try:
                    num = int(num)
                except:
                    num = 0
                args += [ num ]
            try:
                ret = number_intervals( *args )
            except:
                raise template.TemplateSyntaxError, \
                        'Wrong Arguments for intervals: %s' % ','.join( args )
        else:
            kwargs = {}
            args = args_split_list( self.var_args, single_no_list = True )
            for k, value in args.iteritems():
                try:
                    num = int( retrieve_value( value, context, 0 ) )
                except:
                    num = 0
                kwargs[k] = num
            try:
                ret = number_intervals(**kwargs)
            except:
                raise template.TemplateSyntaxError, \
                    'Wrong Arguments for intervals (keybased): %s' % kwargs                
        context[self.var_asname] = ret
        return ''
        

@register.tag
def intervals_args(parser, token ):
    """
    takes up to five arguments interpreted in this order:
        actual = 1, total = 1, first = 3, around = 2, last = 3, breakpoint = 0
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(.+) as (.+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "You need to specify 'as' variable "
    args = arg.replace('  ', ' ').split(' ')
    final = []
    for x in xrange( len ( args )):
        a = args[x]
        if a.lower() != 'as':
            final += [ a ]
        else:
            return IntervalNode( final, args[x+1] )
    raise template.TemplateSyntaxError, 'illegal arguments for intervals: %s' % ",".join(args)

@register.tag
def intervals(parser, token ):
    """
        intervals with keyword arguments.
        keywords:
            actual = 1, total = 1, first = 3, around = 2, last = 3, breakpoint = 0, fill = 0
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(.+) as (.+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "You need to specify 'as' variable "
    arguments, asname = m.groups()
    if not '=' in arguments:
        return intervals_args(parser, token )
    return IntervalNode( arguments, asname )
    

class PaginateNode( template.Node ):
    def __init__(self, list_object = None, name = None, args = None ):
        self.list_object = list_object
        self.name = name
        self.args = args
        
    def render(self, context):
        if not self.args or not self.name or not self.list_object:
            raise template.TemplateSyntaxError, "You need arguments for pagination."
            return ''
        list_object = retrieve_value( self.list_object, context, None )
        if list_object is None:
            raise template.TemplateSyntaxError, "No List object to paginate."
        kwargs = {}
        args = args_split_list( self.args, single_no_list = True )
        for k, value in args.iteritems():
            try:
                num = int( retrieve_value( value, context, 0 ) )
            except:
                num = 0
            kwargs[k] = num
        try:
            ret = Pagination( list_object, **kwargs )
        except Exception, e:
            print e
            raise template.TemplateSyntaxError, \
                    'Wrong Arguments for intervals (keybased): %s (nested exception: %s)' % (kwargs, e)                
        context[self.name] = ret
        return ''
    
@register.tag
def paginate(parser, token):
    """
        use it to paginate an object with a Pagination Capsule.
        
        syntax is:
            {% paginate list_object name page=x... %}
        
    """
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r needs arguments" % token.contents.split()[0]
    m = re.search(r'(\S+) (\S+) (.+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r could not parse its arguments %s" % (tag_name, arg)
    list_object, name, args = m.groups()
    return PaginateNode(list_object, name, args)


############# FILTER ################

@register.filter
def gettuplestring( value, num ):
    try:
        for i, v in value:
            if str(i) == str(num):
                return v
    except:
        pass
    return ''

@register.filter
@stringfilter
def pagenum( value, num ):
    try:
        value = int(value)
        num = int(num)
        pages = int( value / num )
        if value % num:
            pages += 1
        return pages
    except:
        return ''

@register.filter
@stringfilter
def links(value):
    """
        @todo: email adress filtering (mailto:)
        done: http and https adresses.
        dont forget to striptags before this!
    """
    if 'http://' in value:
        links = re.findall(r'(http://[:.\d\w]+\S+)', value, re.M)
        for link in links:
            value = value.replace( link, '<a href="%s" rel="nofollow">%s</a>' % (link, link) )
    if 'https://' in value:
        links = re.findall(r'(https://[:.\d\w]+\S+)', value, re.M)
        for link in links:
            value = value.replace( link, '<a href="%s" rel="nofollow">%s</a>' % (link, link) )
    return mark_safe(value)

@register.filter
@stringfilter
def string_append( value, append ):
    return u"%s%s" % (value, append)

@register.filter
@stringfilter
def string_prepend( value, prepend ):
    return u"%s%s" % (prepend, value)

@register.filter
@stringfilter
def string_remove( value, what ):
    return value.replace( what, '' )

@register.filter
@stringfilter
def search(value, matchstr):
    if re.search( matchstr, value):
        return True
    return False


@register.filter
@stringfilter
def match(value, matchstr):
    if re.match( matchstr, value):
        return True
    return False

@register.filter
@stringfilter
def strip(value, stripv = None):
    try:
        return value.strip(stripv)
    except:
        return value

@register.filter
@stringfilter
def xrange0(value):
    """
    Returns a list with xrange
    First Item is 0
    e.g.: for i in something.count|xrange
    """
    try:
        i = int(value)
        return list(xrange(i))
    except:
        return []

@register.filter
@stringfilter
def xrange1(value):
    """
    Returns a list with xrange
    First Item is 1.
    """
    try:
        i = int(value)
        return [x+1 for x in xrange(i)]
    except:
        return []

   
@register.filter
@stringfilter
def gte(value, as_int):
    try:
        if int(value) >= int(as_int):
            return True
        return False
    except:
        return ''

@register.filter
@stringfilter
def gt(value, as_int):
    try:
        if int(value) > int(as_int):
            return True
        return False
    except:
        return ''

@register.filter
@stringfilter
def lte(value, as_int):
    try:
        if int(value) <= int(as_int):
            return True
        return False
    except:
        return ''

@register.filter
@stringfilter
def lt(value, as_int):
    try:
        if int(value) < int(as_int):
            return True
        return False
    except:
        return ''

@register.filter
@stringfilter
def eq(value, as_int):
    try:
        if int(value) == int(as_int):
            return True
        return False
    except:
        return ''

@register.filter
def or_this(value, what):
    try:
        if value:
            return value
    except:
        pass
    return what
