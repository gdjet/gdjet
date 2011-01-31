from gdjet.functions import oneslash

def get_dojango_context( request ):
    internal = False
    try:
        from dojango.util.config import Config
        from dojango.context_processors import config
    except:
        internal = True
    
    # internal: try to build our own.
    ret = { 'DOJANGO': {} }
    if internal:
        pass
    else:
        ret = config(request)
        for key in [ 'BASE_MEDIA_URL', 'DOJO_MEDIA_URL',
                    'DOJO_THEME_URL', 'BUILD_MEDIA_URL' ]:
            try:
                ret['DOJANGO'][key] = oneslash(ret['DOJANGO'][key])
            except:
                pass
        return ret
    