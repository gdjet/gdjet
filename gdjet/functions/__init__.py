# -*- coding: utf-8 -*-

def oneslash( apath ):
    if not isinstance(apath, str):
        return apath
    apath = apath.replace('//', '/')
    if ':' in apath:
        apath = apath.replace('http:/', 'http://', 1)
        apath = apath.replace('https:/', 'https://', 1)
        apath = apath.replace('ftp:/', 'ftp://', 1)
        apath = apath.replace('file:/', 'file:///', 1)
    return apath
