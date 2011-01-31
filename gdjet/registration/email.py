# -*- coding: utf-8 -*-

# Helper Function for sending emails.
# You want to send a mail in post_registration.

from gdjet import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from gdjet.models.mailer import Email

def send_mail_django( user, code, site=None,
               mail_text_template_file='gdjet/registration/mail.txt',
               mail_html_template_file='gdjet/registration/mail.html',
               subject='Your Activation Code',
               additional_context={} ):
    if user.email:
        try:
            from_email, to = settings.REGISTER_FROM_EMAIL, user.email
            c = Context( { 'user': user, 'code': code } )
            c.update(additional_context)
            text_content = loader.get_template( mail_text_template_file ).render(c)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            if mail_html_template_file:
                html_content = loader.get_template( mail_html_template_file ).render(c)
                msg.attach_alternative(html_content, "text/html")
            msg.send()
            return True
        except Exception, e:
            from gdjet.utils.log import log
            log("Error occured in email %s %s" % (e, e.message), 'gdjet.registration.email_django')
    return False



def send_mail( user, code, site=None,
               mail_text_template_file='gdjet/registration/mail.txt',
               mail_html_template_file='gdjet/registration/mail.html',
               subject='Your Activation Code',
               additional_context={} ):
    if user.email:
        try:
            from_email, to = settings.REGISTER_FROM_EMAIL, user.email
            c = Context( { 'user': user, 'code': code } )
            c.update(additional_context)
            text_content = loader.get_template( mail_text_template_file ).render(c)
            html_content = None
            if mail_html_template_file:
                html_content = loader.get_template( mail_html_template_file ).render(c)
            msg = Email(
                    title = subject,
                    from_email = from_email,
                    text = text_content,
                    html = html_content
                        )
            msg.save()
            msg.add_to(to, user.get_full_name())
            msg.send_or_queue()
            return True
        except Exception, e:
            from gdjet.utils.log import log
            log("Error occured in email %s %s" % (e, e.message), 'gdjet.registration.email')
    return False