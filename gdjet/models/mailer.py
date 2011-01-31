# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from gdjet.models.adminlog import AdminLog
from gdjet import settings

class MailRecipient( models.Model ):
    name = models.CharField( "Name", max_length = 200, blank = True, null = True, )
    mail = models.EmailField( "Email", max_length = 200 )
    
    def __unicode__(self):
        return self.email()
    
    def email(self):
        # @todo: Name <email>
        return self.mail
    
    class Meta:
        app_label = "gdjet"
        verbose_name = "Email Recipient"
        verbose_name_plural = "Email Recipients"

class MailHeader( models.Model ):
    name = models.CharField( "Name", max_length = 100 )
    data = models.CharField( "Data", max_length = 200, blank = True, default = "" )
    def __unicode__(self):
        return u"%s = %s" % (self.name, self.data)
    
    class Meta:
        app_label = "gdjet"
        verbose_name = "Email Header String"
        verbose_name_plural = "Email Header Strings"
    
class Email( models.Model ):
    title = models.CharField("Title", max_length = 200, default = "" )
    from_email = models.EmailField("From Email", max_length = 200 )
    to = models.ManyToManyField( MailRecipient, verbose_name = "To", null = True,
                                 related_name = "emails_to" )
    cc = models.ManyToManyField( MailRecipient, 
                                 verbose_name = "Carbon Copy (Defunct: Use BCC or To)", 
                                 null = True, blank = True,
                                 related_name = "emails_cc" )
    bcc = models.ManyToManyField( MailRecipient, 
                                  verbose_name = "Black Carbon Copy", 
                                  null = True, blank = True,
                                  related_name = "emails_bcc" )
    headers = models.ManyToManyField( MailHeader, 
                                      verbose_name = "Headers", 
                                      null = True, 
                                      blank = True)
    text = models.TextField("Text", default = "" )
    html = models.TextField("Html", default = None, 
                            null = True, blank = True )
    sent = models.DateTimeField( "Sent at", default = None, 
                                 null = True, blank = True )
    send_at = models.DateTimeField( "Send at", default = datetime.now )
    send_fail_count = models.IntegerField( "Failed Attempts", default = 0 )
    
    def add_to(self, email, name = None ):
        obj, created = MailRecipient.objects.get_or_create( 
                                                mail = email,
                                                name = name )
        if created:
            obj.save()
        self.to.add(obj)
        self.save()
    
    def __unicode__(self):
        return u"Email from %s to be sent at %s with title: %s" % (self.from_email, self.send_at, self.title)
        
    def attach(self, filename, data, mimetype = None ):
        MailAttachement( filename = filename,
                       mimetype = mimetype,
                       data = data,
                       mail = self ).save()
    
    def attach_file(self, filepath, mimetype = None ):
        MailAttachementFilepath( filepath = filepath, mimetype = mimetype,
                                 mail = self ).save()

    def send(self, forced = False, failraise = False, adminlog = True ):
        """
            Sends an Email
                forced: do not check if mail is to be sent here (not used yet)
                failraise: raise the exception again if it happens.
                adminlog: log with AdminLog
        """
        try:
            text_content = self.text
            html_content = self.html
            to = [ o.email() for o in self.to.all() ]
            bcc = [ o.email() for o in self.bcc.all() ]
            cc = [ o.email() for o in self.cc.all() ]
            headers = {}
            for header in self.headers.all():
                headers.update( { header.name: header.data } )
            msg = EmailMultiAlternatives(self.title, text_content, self.from_email, to = to,
                    bcc = bcc, headers = headers )
            if html_content:
                msg.attach_alternative(html_content, "text/html")
            for attachement in self.attachements.all():
                msg.attach(attachement.filename, 
                           attachement.data, 
                           attachement.mimetype )
            for attachement in self.attachements_filepath.all():
                msg.attach_file( attachement.filepath,
                                 attachement.mimetype )
            if not settings.MAILER_SKIP_MAILING:
                msg.send()
        except Exception, e:
            if settings.MODULE_ADMINLOG and adminlog:
                try:
                    AdminLog(by = "gdjet.email.send", 
                             message = "Email (%s) could not be sent\nCause: %s" % (self.id, e),
                             severity = 30,
                             ).save()
                except:
                    pass
            self.send_fail_count += 1
            self.save()
            if failraise:
                raise e
            return False
        if not settings.MAILER_SKIP_MAILING:
            self.sent = datetime.now()
        self.save()
        return True
    
    def send_or_queue( self, failraise = False, adminlog = True,  ):
        if self.send_at <= datetime.now():
            return self.send( adminlog = adminlog, failraise = failraise)
        else:
            self.save()
            return True
    
    class Meta:
        app_label = "gdjet"
        
# @todo: mailfileattachment.

class MailAttachement( models.Model ):
    mail = models.ForeignKey(Email, related_name = "attachements")
    filename = models.CharField("Filename", max_length = 200, default = "attachement" )
    mimetype = models.CharField("MIME", max_length = 100, default = "text/plain" )
    data = models.TextField()
    
    def __unicode__(self):
        return "%s (%s)" % (self.filename, self.mimetype)
    
    class Meta:
        app_label = "gdjet"
        verbose_name = "Email Attachement"
        verbose_name_plural = "Email Attachements"

class MailAttachementFilepath( models.Model ):
    mail = models.ForeignKey( Email, related_name = "attachements_filepath")
    filepath = models.CharField( "Path to File", max_length = 200, default = "", help_text = "path to file on server." )
    mimetype = models.CharField( "MIME", max_length = 100, null = True, blank = True )
    
    def __unicode__(self):
        return "Attach: %s" % self.filepath
    
    class Meta:
        app_label = "gdjet"
        verbose_name = "Email Attachement (Filepath)"
        verbose_name_plural = "Email Attachements (Filepath)"#
        