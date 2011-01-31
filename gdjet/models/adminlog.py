# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime

class AdminLog( models.Model ):
    date = models.DateTimeField("Time", default = datetime.now )
    by = models.CharField("Issued by", max_length = 100, default = "Unknown" )
    severity = models.IntegerField("Severity", default = 10 )
    message = models.TextField( "Message", default = "" )
    
    
    def __unicode__(self):
        return "Log at %s by %s" % (self.date, self.by)
    
    class Meta:
        app_label = "gdjet"
        verbose_name = "Fehler"
        verbose_name_plural = "Fehlerprotokoll"
