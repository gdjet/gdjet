
import os
try:
    from filebrowser.settings import *
except:
    CONVERT_FILENAME = True

def convert_filename_fix(value):
    """
    Convert Filename.
    """
    
    if CONVERT_FILENAME:
        # advanced conversion:
        # slower but painless.
        val = u''
        value = value.replace(" ", "_").lower()
        for c in value:
            if c in 'abcdefghijklmnopqrstuvwxyz.1234567890_-':
                val += c
        if not val:
            raise Exception("Filename without value %s -> %s" % (value, val) )
        elif val.startswith('.'):
            val = u'something_%s' % val
        return val
    else:
        return value

# monkeypatch:
try:
    from filebrowser import functions
    functions.convert_filename = convert_filename_fix
    # functions.convert_filename = convert_filename
except:
    pass