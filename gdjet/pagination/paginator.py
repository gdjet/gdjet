# -*- coding: utf-8 -*-
from gdjet.utils.intervals import number_intervals
from gdjet.settings import PAGINATOR_STANDARD_TEMPLATE

class Pagination( object ):
    """
        Pagination Object helps you to paginate Queries or other iterables.
        
        normal usecase:
            p = Pagination( query, per_page = 10, actual = 1 )
            
        If you set "real_count" it means, the paginated object is already
        just a subset of itself (presliced).
        
        from there on:
        p.get_slice() will get the slice of the actual page.
        p.intervals() will output intervals like gdjet intervals function
        p.page_range() returns 1..pagenumber
        
        Note: kwargs is directly used to create intervals.
        (first, around, breakpoint, fill)
    """
    
    paginated_object = None
    count = None #total object count.
    pages_num = None #total number of pages.
    actual = None
    
    __presliced = False # whether the paginated object is already sliced.
    __per_page = 1
    __intervals = None
    __template = PAGINATOR_STANDARD_TEMPLATE
    DEFAULT_TO_FIRST_PAGE = True # whether "no" page will go to page 1.
    
    def __init__( self, 
                  paginated_object = None, 
                  per_page = 1, 
                  actual = 1,
                  real_count = None,
                  **kwargs ):
        if real_count:
            # this is something else.
            self.__presliced = True
        if paginated_object:
            self.set_paginated_object( paginated_object, real_count )
        self.per_page = per_page
        self.actual = actual or 1
        self.kwargs = kwargs
    
    # setters, getters, inner functions, init
    def calc_pages_num(self):
        try:
            pages_num = int( self.count / self.per_page )
            if self.count % self.per_page:
                pages_num += 1
        except:
            pages_num = 0
        self.pages_num = pages_num
    
    def set_paginated_object( self, o, count = None ):
        self.paginated_object = o
        if count is None and not self.__presliced:
            if hasattr(o, 'count'):
                if callable( getattr(o, 'count') ):
                    try:
                        count = o.count()
                    except:
                        count = o.__len__()
                else:
                    count = o.count
            else:
                count = o.__len__()
        self.count = count
        if not self.count:
            self.count = 0
        self.calc_pages_num()
        self.__intervals = None
    
    def set_per_page(self, num):
        if not num:
            num = 1
        self.__per_page = num
        self.calc_pages_num()
    
    def get_per_page(self, ):
        return self.__per_page
    # why? because setting per_page will update num_pages
    per_page = property(get_per_page, set_per_page)
    
    def get_template(self):
        return self.__template
    
    def set_template(self, template_name):
        self.__template = template_name
    template = property( get_template, set_template )
    
    
    # django compatibility.
    def page_range( self ):
        return range(1, self.pages_num+1)
    # @todo: all of them.
    
    # helpers for templates
    def get_slice( self, page = None ):
        # if page is none, we take the actual page if given.
        if self.__presliced:
            return self.paginated_object
        offset = self.get_offset(page)
        return self.paginated_object[offset:offset+self.per_page]
    
    def get_offset(self, page = None ):
        if page > self.pages_num:
            page = self.pages_num
        if not page:
            if not self.actual:
                # no actual page. this probably means, this paginator is not well called.
                if self.DEFAULT_TO_FIRST_PAGE:
                    page = 1
                else:
                    raise Exception("No actual Page in Paginator.")
            else:
                page = self.actual or 1
        if page > self.pages_num:
            page = self.pages_num
        if page <= 0:
            page = 1
        offset = (page-1) * self.per_page
        return offset
    # intervals compatibility.
    
    def set_intervals(self, first = 3, around = 2, last = 3, breakpoint = 0, fill = 0, **kwargs):
        adict = { 'first': first,
                  'around': around,
                  'last': last,
                  'breakpoint': breakpoint,
                  'fill': fill,                       
                       }
        if not self.kwargs:
            self.kwargs = adict
        else:
            self.kwargs.update(adict)
    
    def intervals(self):
        if not self.__intervals:
            args = {
                'total': self.pages_num,
                'actual': self.actual, # first=1 around=4 last=1 breakpoint=9 fill=9
                'first': 1,
                'around': 4,
                'last': 1,
                'breakpoint': 9,
                'fill': 9,
                    }
            args.update(self.kwargs)
            self.__intervals = number_intervals(**args)     
        return self.__intervals