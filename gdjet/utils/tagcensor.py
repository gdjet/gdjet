# -*- coding: utf-8 -*-
"""
    TagCensor
    (C) by Gabor Gumics 2010
    Part of Gdjet. See gdjet/license.txt
    
    @author: Gabor Guzmics <gab@g4b.org>
    
    Description:
        This Library allows you to validate a HTML source by checking in
        a dictionary, if tags are allowed to be used.
        
        It can be configured to allow certain tags, narrow them by allowing
        only certain attributes, and narrow them even more by allowing them
        only certain attribute-values.
        
        The Format of this configuration is atm:
        {
            'tag1': { 'attribute1': [ 'value_it_can_have1' ] },
            'tag2': { 'attribute2': [ 'value_it_can_have1',
                                      'value_it_can_have2', ],
                      'attribute3_can_have_any_value': True },
        }
        and so on, see _tags_allowed_example for more config settings.
        
        It has the extra features of:
            * learning the basic structure of the tags by analyzing html
              (can be used for other purposes too)
            * parsing the allowed_tags from tinymce valid_elements
            * building valid_elements for tinymce as string
"""

import re
try:
    from lxml import etree
    # no verbosity on success.
    # print("running with lxml.etree")
except ImportError:
    try:
    # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
        # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")
                    
_tags_allowed_example = {
    '__all__': [ 'class', 'id' ], # all (except None) can have these attributes.
    # should be used carefully.
    'a':        {'href': True, # can be anything.
                 'target': ['_blank', ], # can have only _blank as value for target 
                 # None might make problems in the list.
                },
    'b':        False, # use __all__, no specific limitation.
    'p':      { 'src': True },
    'body':     None, # can't have ANY attributes.
    'p':        False, # can only have __all__ attributes.
    'img':      { 'src': True }, # can have src, which can have any value.
    'i':        True, # can have any attribute you want.
                }

class InvalidData( Exception ):
    """
        Exception thrown by tagcensor.
        It holds a message, which might tell you more about the problem
        and an update_dict, which might suggest how to update your allowed_tags
        to get this problem away.
    """
    message = ""
    update_dict = {}
    def __init__(self, message, update_dict = {}, *args, **kwargs):
        self.message = message or ''
        self.update_dict = update_dict
        return super( InvalidData, self).__init__(*args, **kwargs)

def build_allowed_tags( tinymce_valid_elements ):
    """
        takes the string from tinymce valid_elements setting,
        disects it and builds the internal dictionary format
        out of it.
    """
    groups = tinymce_valid_elements.split(',')
    ret = {}
    for igroup in groups:
        realgroups = []
        mg = igroup.split('/')
        if len(mg)>1:
            l = mg[-1].split('[')
            if len(l)>1:
                l = "[%s" % l[1]
            else:
                l = ''
            realgroups = [ "%s%s" % ( g, l ) for g in mg  ]
        else:
            realgroups = [igroup]
        for group in realgroups:
            m = re.search(r'^(\w+)$', group)
            if not m:
                try:
                    m = re.search(r'^(\w+)\[(\S+)\]$', group)                    
                    tagname, attribs = m.groups()
                    attribs = attribs.split('|')
                except Exception, e:
                    print e
                    print group
                    print attribs
                    raise Exception("Invalid Tag in tinymce valid_elements")
            else:
                attribs = False
            tagname = m.groups()[0]
            new_attribs = {}
            if attribs:
                for attrib in attribs:
                    if '<' in str(attrib):
                        attrib, allowed = attrib.split('<')
                        allowed = allowed.split('?')
                        new_attribs[attrib] = allowed
                    else:
                        new_attribs[attrib] = None
            ret[tagname] = new_attribs or True
    return ret

def build_tinymce_valid_elements( allowed_tags ):
    """
        builds a tinymce string out of the internal format.
        __all__ is added to all lists there are.
        Note, that if an element has no list, but other settings
        maybe specific to this library, or to your needs, it might
        get simply added as "allowed tag".
    """
    add_to_all = allowed_tags.get('__all__', None)
    s = []
    for tagname in allowed_tags.keys():
        if tagname.startswith('__'):
            continue
        attribs = allowed_tags.get( tagname, None )
        if attribs:
            a = []
            for attrib in attribs.keys():
                allowed = attribs[attrib] 
                if isinstance(allowed, basestring):
                    if add_to_all:
                        allowed = allowed + add_to_all
                        allowed = "<%s" % "?".join( allowed )
                    else:
                        allowed = "<%s" % allowed
                if isinstance( allowed, list ):
                    if add_to_all:
                        allowed = allowed + add_to_all
                    allowed = "<%s" % "?".join( allowed )
                else:
                    allowed = None
                a += [ "%s%s" % ( attrib, allowed or '' ) ]
            attribs = "[%s]" % "|".join(a)
        s += [ "%s%s" % (tagname, attribs or '') ]
    return ",".join(s)
            
                 

def check_children( root, tags_allowed ):
    """
        checks the children of a node against allowed tags.
    """
    for child in root:
        if child.tag not in tags_allowed.keys():
            udict = {child.tag: {}}
            raise InvalidData('Tag not allowed: %s' % child.tag,
                              udict )
        else:
            if len( child ) > 0:
                check_children(child, tags_allowed)
            # check attributes.
            attribs = child.attrib
            allowed = {}
            if tags_allowed[child.tag] is True:
                continue
            elif tags_allowed[child.tag] is None:
                if len( attribs ) > 0:
                    udict = {child.tag: {}}
                    raise InvalidData( 'Tag %s cannot have attributes.' % child.tag,
                                       udict )
                else:
                    continue
            elif tags_allowed[ child.tag ] is False:
                pass
            else:
                allowed.update( tags_allowed[child.tag] )
            allowed.update( tags_allowed.get( '__all___', {}) )
            allowed_keys = allowed.keys()
            for k in attribs.keys():
                if k in allowed_keys:
                    if isinstance( allowed[k], list ):
                        if attribs.get(k, None) not in allowed[k]:
                            n = {}
                            n.update(allowed)
                            n.update({k: allowed[k] + [attribs.get(k, None)]})
                            udict = { child.tag: n }
                            raise InvalidData( 'Tag %s attrib %s is not allowed to have %s' % 
                                               ( child.tag,
                                               k,
                                               attribs.get(k, None) ),
                                               udict )
                    elif isinstance(allowed[k], basestring):
                        if not attribs.get(k, None) == allowed[k]:
                            n = {}
                            n.update(allowed)
                            n.update({k: [allowed[k]] + [attribs.get(k, None)]})
                            udict = { child.tag: n }
                            raise InvalidData( 'Tag %s attrib %s is not allowed to have' % 
                                               ( child.tag, 
                                                 k,
                                                 attribs.get(k, None) ),
                                                udict)
                else:
                    n = {}
                    n.update(allowed)
                    n.update({k: []})
                    udict = { child.tag: n }
                    raise InvalidData( 'Tag %s attrib %s is not allowed' % ( child.tag, k, ),
                                       udict)

def check_html( source, tags_allowed, reraise = False ):
    """
        checks a html and fails if any error happens.
        returns False on fail, True on success.
        reraises Exception if reraise is true.
    """
    parser = etree.HTMLParser()
    document = etree.fromstring( u"<html><body>%s</body></html>" % source, parser )
    body = document[0]
    try:
        check_children(body, tags_allowed)
    except InvalidData, e:
        # print e.message
        if reraise:
            raise
        return False
    return True

def check_html_learn( source, tags_allowed = {} ):
    """
        checks a html, but as often as it succeeds, while
        adding all the rules not succeeding automatically to
        tags_allowed.
        returns the built ruleset at the end.
        raises Exception if learning did not work.
        might cause endless loops in certain situation, use this carefully.
    """
    parser = etree.HTMLParser()
    document = etree.fromstring( u"<html><body>%s</body></html>" % source, parser )
    body = document[0]
    done = False
    while not done:
        try:
            check_children(body, tags_allowed)
            done = True
        except InvalidData, e:
            # add udict.
            # retry whole process.
            n = {}
            n.update(tags_allowed)
            n.update(e.update_dict)
            if n == tags_allowed:
                print body
                print tags_allowed
                print n
                raise Exception("Could not learn nothing.")
            tags_allowed = n
    return tags_allowed
