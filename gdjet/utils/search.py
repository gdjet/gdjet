
from django.db import models
from gdjet.utils.db import Q, EmptyQ
from gdjet.utils.strings import isplit

import re

NOT_TOKENS = ['NOT']
AND_TOKENS = ['AND']
OR_TOKENS = [ 'OR' ]

class SearchResult( object ):
    """
        Dict-Like Object to save search results.
    """
    def __init__(self, s):
        self.s = s
    
    def reset(self):
        """
            resets this search result.
            does nothing here, but used in cache.
        """
        pass
    
    def all(self):
        return self.s.do_search()
    
    def keys(self):
        return self.s.search_models.keys()
    
    def __getitem__(self, name ):
        if name == 'all':
            return self.all()
        return self.s.do_search( name )
    
    # futuretech: filter, exclude, ...
    def filter(self, **kwargs ):
        """
            returns all search results with an additional filter.
        """
        pass
    
    
class SearchResultCached( SearchResult ):
    """
        SearchResult with Cache.
        Holds on to it's Queries, so django can cache them itself.
        Does NOT cache search RESULTS, only the QUERY OBJECTS.
    """
    cached = {}
    def __init__(self, s):
        SearchResult.__init__(self, s)
        self.reset()
    
    def reset(self):
        self.cached = {}
    
class SearchTerm( object ):
    """
        A Search Term.
        Knows how to tokenize SearchTerms.
    """
    hooks = {} # contains a list of hooks in the searchterm
    
    def __init__(self, searchterm ):
        self.searchterm = searchterm
        self.hooks = self.search_hooks()
    
    def search_hooks(self):
        ret = {}
        tokens = isplit(self.searchterm, True )
        for token in tokens:
            hookfound = re.match(r'^\w+:\w+$', token)
            if hookfound:
                h = hookfound.group().split(':')
                ret[ h[0] ] = h[1]
        return ret
    
    def tokenize(self, exclude_hooks = [] ):
        tokens = isplit(self.searchterm, True)
        
        next_not = False
        next_and = False
        last = None
        and_line = None
        not_line = []
        or_line = []
        for token in tokens:
            # we ignore hooks. we check if spaces are inside, since
            # hooks dont accept spaces, so we filter "hook:to something"
            for hook in exclude_hooks:
                if token.startswith( '%s:' % hook ) and ' ' not in token:
                    continue
            if token in NOT_TOKENS:
                next_not = True
                next_and = False
                continue
            if token in AND_TOKENS:
                next_and = True
                next_not = False
                continue
            if token in OR_TOKENS:
                next_and = False
                continue
            if token.startswith('-'):
                next_not = True
                next_and = False
                token = token[1:]
                if not token:
                    continue
            # check if this is AND:
            if next_and:
                if and_line:
                    and_line += [ token ]
                else:
                    if last:
                        and_line = [ last, token ]
                    else:
                        and_line = [ token ]
                next_and = False
                last = and_line
                continue
            if next_not:
                not_line += [ token ]
                next_not = False
                continue
            if last:
                if isinstance(last, list):
                    or_line += [ last, ]
                else:
                    or_line += [[ last, ]]
            last = token
        if last:
            if isinstance(last, list):
                or_line += [ last, ]
            else:
                or_line += [[ last, ]]
        print (or_line, not_line)
        return (or_line, not_line)

class Sf( object ):
    _name = None
    _op = 'icontains'
    def __init__(self, name):
        self._name = name
        
    def name(self):
        return self._name
    def op(self):
        return self._op
    def q(self, something ):
        return Q( **{ "%s__%s" % (self._name, self._op ): something } )

class Sfint(Sf):
    """
        integer search.
    """
    _op = 'exact'
    _positive = False # True False
    _rangecheck = False # False or (min, max) # [min-]max
    def q(self, something):
        try:
            i = int(something)
            if self._positive and i < 0:
                return EmptyQ()
            if self._rangecheck:
                min, max = self._rangecheck
                if i < min or i >= max:
                    return EmptyQ()
            return Q( **{ "%s__%s" % (self._name, self._op): i  } )
        except:
            return EmptyQ()

class Sffloat(Sf):
    """
        float search.
    """
    _op = 'exact'
    _positive = False # True False
    _rangecheck = False # False or (min, max) # [min-]max
    def q(self, something):
        try:
            f = float(something)
            if self._positive and f < 0.0:
                return EmptyQ()
            if self._rangecheck:
                min, max = self._rangecheck
                if f < float(min) or f >= float(max):
                    return EmptyQ()
            return Q( **{ "%s__%s" % (self._name, self._op): f  } )
        except:
            return EmptyQ()

class Sfdate(Sf):
    """
        date search.
    """
    pass # @todo: implement smart date check of the string.

class S( object ):
    search_models = {} # saves the model instances / queries we want to search.
    search_fields = {} # saves the fields in the model to be searched.
    searchterm = ""
    results = None
    
    def __init__(self, searchterm = "" ):
        self.results = SearchResultCached( self,  )
        self.searchterm = SearchTerm( searchterm )
        
    def add_model(self, model_name, model, fields ):
        self.search_models[model_name] = model
        self.search_fields[model_name] = []
        for field in fields:
            if isinstance(field, str):
                self.search_fields[model_name] += [ Sf( field ) ]
            elif isinstance(field, Sf):
                self.search_fields[model_name] += [ Sf( field ) ]
            elif isinstance(field, models.IntegerField):
                self.search_fields[model_name] += [ Sfint( field ) ]
            elif isinstance(field, models.FloatField):
                self.search_fields[model_name] += [ Sffloat( field ) ]
            
            # @todo: auto determine more django model fields.
            
    def search(self, something):
        self.searchterm = SearchTerm( something )
        return self.do_search()
    
    def do_search( self, model_only = None ):
        tokens, not_tokens = self.searchterm.tokenize()
        ret = []
        for model_name in self.search_models.keys():
            if model_only and model_only != model_name:
                continue
            M = self.search_models[ model_name ]
            f = None # saves our filters.
            n = None # saves our excludes.
            positive = []
            negative = []
            for field in self.search_fields[ model_name ]:
                for or_token in tokens:
                    f_and = None
                    for and_token in or_token:
                        if f_and:
                            f_and &= field.q( and_token )
                        else:
                            f_and = field.q( and_token )
                    if f: # already got some Q objects.
                        f |= f_and
                    else: # create first.
                        f = f_and
                for not_token in not_tokens:
                    if n: # already got one
                        n &= field.q( not_token )
                    else: # create it
                        n = field.q( not_token )
                if f or n: # if both not, there was no query to make.
                    query = None
                    if isinstance(M, models.Model):
                        query = M.objects # if its just the model, we search objects.
                    else:
                        query = M # else we search the model - which is a query...
                if f:
                    positive.extend( query.filter( f ).values_list( 'pk', flat = True ) )
                    f = None
                if n:
                    negative.extend( query.filter( n ).values_list( 'pk', flat = True) )
                    n = None
            ret += [ query.filter( pk__in = positive).exclude( pk__in = negative) ]
        return ret
    
