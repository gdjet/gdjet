# -*- coding: utf-8 -*-

def cmyk_to_rgb_simple( cmykarray ):
    """
        Simple CMYK->RGB conversion
        AdobePhotoshop does this 
        
    """
    return [ 255-min( 255, cmykarray[0] + cmykarray[3] ), 
            255-min( 255, cmykarray[1] + cmykarray[3] ), 
            255-min( 255, cmykarray[2] + cmykarray[3] ) ]

def cmyk_to_rgb_affin( cmykarray ):
    """
        Affin CMYK->RGB Conversion
        GNU GhostScript does this.
        it supposed to be better, but is slower.
    """
    colors = 255 - cmykarray[3]
    return [ max(0, int(colors * (255-cmykarray[0])/255.0)),
             max(0, int(colors * (255-cmykarray[1])/255.0)),
             max(0, int(colors * (255-cmykarray[2])/255.0)),
            ]

cmyk_to_rgb=cmyk_to_rgb_affin