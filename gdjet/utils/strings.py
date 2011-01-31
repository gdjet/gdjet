# -*- coding: utf-8 -*-
"""
    String Helpers.
    @author g4b
"""
import re

def tuple_string( tup, index, default = None, translate = 'utf-8' ):
    for (k, v) in tup:
        if k == index:
            if translate and hasattr(v, 'translate'):
                return v.translate(translate)
            return v
    return default

def isplit( something, strip_quotes = False ):
    """
    intelligent split.
        splits strings by spaces but keeps quotes intact.
    
    modified from:
    http://stackoverflow.com/questions/79968/split-a-string-by-spaces-preserving-quoted-substrings-in-python
    
    """
    if strip_quotes:
        return [i.strip('"').strip("'") for i in 
                re.split(r'(\s+|(?<!\\)".*?(?<!\\)"|(?<!\\)\'.*?(?<!\\)\')', 
                            something) if i.strip()]        
    return [i for i in re.split(r'(\s+|(?<!\\)".*?(?<!\\)"|(?<!\\)\'.*?(?<!\\)\')', 
                            something) if i.strip()]

def args_split( something ):
    """
        this function tries to find argument based strings
        like:
        var1=varX var2='test','this',varZ
        it returns:
        { 'var1': 'varX',
          'var2': "'test','this',varZ"
        }
    """
    # we split the string inteligently
    args = isplit(something)
    # we have to reverse this, because we want to find extra parts
    # since things like a='a','b' gets split into ["a=", "'a'", ",", "'b'" ]  
    args.reverse()
    arg_dict = {}
    last_combine = []
    for arg in args:
        # check if there is a = inside and the first part does not contain ' or "
        # we need that to ensure, this is not a quoted string.
        parts = arg.split("=")
        if len(parts) == 1:
            last_combine += [ arg ]
        elif len(parts) > 1:
            if (parts[0].find('"') > -1) or (parts[0].find("'") > -1):
                 last_combine += [ arg ]
            else:
                last_combine.reverse()
                last_combine = parts[1:] + last_combine
                arg_dict[str(parts[0])] = "".join( last_combine )
                last_combine = []
        else:
            raise Exception("Empty Argument found? That IS weird: %s in %s" % ( args, something ))
    
    return arg_dict

def args_split_list(something, single_no_list = False):
    """
        splits the variables of args_split into a list of arguments by comma.
        
        if single_no_list ist given, singletons are not represented as a list
        with one member.
        
        @see args_split
        this returns:
        { 'var1': ['varX'],
          'var2': ["'test'", "'this'", "varZ" ],
        }
    """
    splitted = args_split(something)
    for key in splitted.keys():
        if splitted[key].startswith('[') and splitted[key].endswith(']'):
            splitted[key] = splitted[key][1:-1].split(',')            
        else:
            if single_no_list:
                if not ',' in splitted[key]:
                    continue
            splitted[key] = splitted[key].split(',')
    return splitted
