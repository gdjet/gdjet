from django.db import models

class Vcss( models.Model ):
    url = models.CharField( u'URL', max_length = 254, help_text="don't use extension .css" )
    data = models.TextField( u'Data', blank = True, null = True)
    def __unicode__(self):
        return "CSS: %s.css" % self.url
    class Meta:
        app_label = 'gdjet'

class Vjs( models.Model ):
    url = models.CharField( u'URL', max_length = 254, help_text= "don't use extension .js" )
    data= models.TextField(u'Data', blank = True, null = True )
    def __unicode__(self):
        return "JS: %s.js" % self.url
    class Meta:
        app_label = 'gdjet'

class Vtemplate( models.Model ):
    url = models.CharField( u'template_name', max_length = 254 )
    data= models.TextField(u'Data', blank = True, null = True )
    def __unicode__(self):
        return "Template: %s" % self.url
    class Meta:
        app_label = 'gdjet'

class Vredirect( models.Model ):
    url = models.CharField( u'URL', max_length = 254 )
    wildcard = models.CharField( u'Wildcard', max_length = 100, blank = True, null = True)
    redirect_to = models.CharField( u'Redirect URL', max_length = 254 )
    def __unicode__(self):
        return "redir: %s -> %s" % (self.url, self.redirect_to)
    class Meta:
        app_label = 'gdjet'
