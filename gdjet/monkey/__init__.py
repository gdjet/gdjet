from gdjet import settings

if settings.MODULE_MONKEY:
    for key in settings.MODULE_MONKEY.keys():  #@UndefinedVariable
        val = settings.MODULE_MONKEY[key]
        if 'filebrowser_scale_and_crop' in key and val:
            from filebrowser_scale_and_crop import *
        elif 'filebrowser_convert_filename' in key and val:
            from filebrowser_convert_filename import *
            
