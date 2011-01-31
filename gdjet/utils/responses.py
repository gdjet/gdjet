# -*- coding: utf-8 -*-
from django.utils.cache import md5_constructor
from django.http import HttpResponse

def file_response( filename, data, mimetype = 'application/octet-stream',
                   response = None ):
    """
        sends a file as response.
    """
    if not response:
        response = HttpResponse(mimetype=mimetype)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response.write( data )
    try:
        md_data = unicode ( data, errors='ignore')
    except:
        md_data = data
    response['ETag'] = '"%s"' % md5_constructor( md_data ).hexdigest() 
    return response
