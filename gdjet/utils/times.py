# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta #@UnresolvedImport
import time

def next_week( by = None ):
    if not by:
        by = datetime.now().date()
    return by + relativedelta(weeks = 1)

def next_month( by = None ):
    if not by:
        by = datetime.now().date()
    return by + relativedelta(months = 1)

def tomorrow( by = None ):
    if not by:
        by = datetime.now().date()
    return by + relativedelta(days = 1)

def yesterday( by = None ):
    if not by:
        by = datetime.now().date()
    return by - relativedelta(days = 1)

def last_week( by = None ):
    if not by:
        by = datetime.now().date()
    return by - relativedelta(weeks = 1)

def in_hours( hours = 1, by = None ):
    if not by:
        by = datetime.now()
    if hours < 0:
        return by - relativedelta( hours = abs(hours) )
    return by + relativedelta( hours = abs(hours) )

def in_minutes( minutes = 1, by = None ):
    if not by:
        by = datetime.now()
    if minutes < 0:
        return by - relativedelta( hours = abs(minutes) )
    return by + relativedelta( hours = abs(minutes) )

def in_days( days = 2, by = None ):
    if not by:
        by = datetime.now().date()
    if days < 0:
        return by - relativedelta(days = abs( days ) )        
    return by + relativedelta(days = days)

def in_weeks( weeks = 2, by = None ):
    if not by:
        by = datetime.now().date()
    if weeks < 0:
        return by - relativedelta(weeks = abs( weeks ) )
    return by + relativedelta(weeks = weeks)

def in_months( months = 2, by = None ):
    if not by:
        by = datetime.now().date()
    if months < 0:
        return by - relativedelta(months = abs( months ) )        
    return by + relativedelta(months = months)

def days_ago( days = 2, by = None ):
    if not by:
        by = datetime.now().date()
    return by - relativedelta(days = days)

def mk_date_time( dateString, strFormat="%Y-%m-%d"):
    eSeconds = time.mktime( time.strptime( dateString, strFormat ))
    return datetime.fromtimestamp(eSeconds)

def first_of_month( dt ):
    return mk_date_time( "%04d-%02d-01" % ( dt.year, dt.month ) )

def last_of_month( dt ):
    year = dt.year
    month = dt.month
    if dt.month == 12:
        year += 1
        month = 1
    else:
        month += 1
    next_first = mk_date_time( "%04d-%02d-01" % (year, month) )
    return days_ago( 1, next_first )

def smart_date( datestring, by = None ):
    """
        smart date tries to decode a string.
        you can say things like "tomorrow"
        or "days+1"
        you can also add a 'by' date which represents "today".
        
    """
    if not by:
        by = datetime.now().date()
    if not isinstance(datestring, str):
        return by
    datestring = datestring.lower().replace(' ', '')
    # fixed constants:
    if datestring.lower() in ['heute', 'today', 'present']:
        return by
    elif datestring.lower() in ['tomorrow', 'morgen']:
        return tomorrow(by)
    elif datestring.lower() in ['yesterday', 'gestern']:
        return yesterday(by)
        
    # dynamics:
    if datestring.startswith('days'):
        # days+-X
        int_part = datestring[4:]
        try:
            i = int( int_part.strip() )
            return in_days( i, by = by )
        except:
            raise Exception( "gdjet.smart_date: Integer Part of %s is faulty."\
                             "You have to use 'days+<Num>' or 'days-<Num>'." % datestring )
    elif datestring.startswith('weeks'):
        # weeks+-X
        int_part = datestring[5:]
        try:
            i = int( int_part.strip() )
            return in_weeks( i, by = by )
        except:
            raise Exception( "gdjet.smart_date: Integer Part of %s is faulty."\
                             "You have to use 'weeks+<Num>' or 'weeks-<Num>'." % datestring )
    elif datestring.startswith('months'):
        # months+-X
        int_part = datestring[6:]
        try:
            i = int( int_part.strip() )
            return in_months( i, by = by )
        except:
            raise Exception( "gdjet.smart_date: Integer Part of %s is faulty."\
                             "You have to use 'months+<Num>' or 'months-<Num>'." % datestring )    
    else:
        # this happens to be a datestr.
        # @todo try to determine which version.
        return datetime.strptime( datestring, "%Y-%m-%d")
    
