try:
    from ho import pisa #@UnresolvedImport
except:
    pass

from StringIO import StringIO
from subprocess import call
from tempfile import mkstemp
from gdjet.models.adminlog import AdminLog
from gdjet import settings
import os

def write_to_temp( what, suffix = '.tmp' ):
    f_s, f_sname = mkstemp( suffix = suffix )
    f_s = open( f_sname, 'wb' )
    f_s.write( StringIO( what ).read() )
    f_s.close()
    return f_sname

def wk_pdf_file( sourcefile, destfile, wk_executable = "wkhtmltopdf", 
                 options = [], del_source = False,
                 ):
    """
        Writes a PDF File and returns the filename.
        options like: [ '-O', 'landscape', '-s', 'a3' ]
    """
    if not destfile.endswith('.pdf'):
        destfile += '.pdf'
    try:
        rc = call( [ wk_executable ] + options + [ sourcefile, destfile ] )
        os.remove( sourcefile )        
        return destfile
    except Exception, e:
        if settings.MODULE_ADMINLOG:
            AdminLog( by = 'gdjet.utils.pdf.wk_pdf_file',
                  message = 'Error writing PDF File: %s\n%s' % (destfile, e) ).save()
        else:
            raise
    return False

def wk_pdf_file_from_html( source, destfile, wk_executable = 'wkhtmltopdf',
                           options = [], del_source = True, ):
    sourcefile = write_to_temp(source, '.html')
    return wk_pdf_file(sourcefile, destfile, wk_executable, options, del_source)

def wk_pdf( source, css, wk_executable = "wkhtmltopdf", del_tmp = False ):
    # create a file out of source
    f_s = None
    f_sname = None
    f_c = None
    f_cname = None
    if source:
        f_s, f_sname = mkstemp( suffix = '.html')
        f_s = open( f_sname, 'wb' )
        f_s.write( StringIO(source).read() )
        f_s.close()
    if css:
        f_c, f_cname = mkstemp( suffix = '.css' )
        f_c = open( f_cname, 'wb' )
        f_c.write( css )
        f_c.close()
    f_o, f_oname = mkstemp(suffix='.pdf')
    r = True # we assume everything goes by-the-book.
    try:
        rc = call( [ wk_executable, '-O', "landscape",  '-s', "a3", f_sname, f_oname ] )
        f = open( f_oname, 'rb' )
        r = f.read()
        f.close()
    except:
        r = False
        raise
    # cleanup mess.
    try:
        if del_tmp:
            os.remove( f_sname )
            if f_cname:
                os.remove( f_cname )
            if f_oname and del_tmp:
                os.remove( f_oname )
    except:
        pass # we dont really care.
    return r

def write_pdf_django( source, css = None, try_wk = False ):
    if try_wk:
        result = wk_pdf( source, css )
        if result:
            return result
    result = StringIO()
    pdf = pisa.pisaDocument(StringIO(
        source), result, encoding='UTF-8', default_css = css ) # .encode("UTF-8")
    return result.getvalue()

