# -*- coding: utf-8 -*-

def number_intervals( actual = None, 
                      total = None, 
                      first = 3, 
                      around = 2, 
                      last = 3, 
                      breakpoint = 0, 
                      fill = 0, **kwargs ):
    if not actual:
        actual = 1
    if not total:
        total = 1
    next, prev = '', ''
    if actual > 1:
        prev = actual - 1
    if actual < total:
        next = actual + 1
    if breakpoint and total < breakpoint:
        return { 'first': [],
                 'last': [],
                 'actual': actual,
                 'total': total,
                 'around': [ i+1 for i in xrange(total) ],
                 'prev': prev,
                 'next': next,
                }
    if first+1 >= actual-around:
        around_begin = 0
        first = []
    else:
        around_begin = actual - around
        first = [ i+1 for i in xrange(first) ]
    if actual+around >= (total-last-1):
        around_end = total
        last = []
    else:
        around_end = actual + around
        last = [ i+1 + (total-last) for i in xrange(last) ]
    if fill:
        while len(range(around_begin, around_end)) < min( fill, total ):
            if around_end < total:
                around_end += 1
            elif around_begin > 1:
                around_begin -= 1
            else:
                break        
    return  {
        'first': first,
        'around': [ i+1 for i in range(around_begin, around_end) ],
        'last': last,
        'actual': actual,
        'total': total,  
        'prev': prev,
        'next': next,
             }
    
