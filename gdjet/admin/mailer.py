from common import *
from gdjet.models.mailer import *

class AttachementInline(admin.StackedInline):
    model = MailAttachement
    extra = 1
    allow_add = True

class AttachementFilepathInline(admin.StackedInline):
    model = MailAttachementFilepath
    extra = 1
    allow_add = True

class EmailAdmin(admin.ModelAdmin):
    list_display = ('title', 'from_email', 'send_at', 'sent', )
    actions = ['action_resend_emails', 'action_send_unsent_emails' ]
    inlines = [ AttachementInline, AttachementFilepathInline ]
    
    fieldsets = (
        ('Headpart', {
            'classes': ('collapse-open',),
            'fields': ( 'title', 'from_email', 'to', 'bcc' ),
        }),
        ('HeadpartExtra', {
            'classes': ('collapse-closed',),
            'fields': ( 'headers', 'cc', 'send_at', 'sent', 'send_fail_count' ),
        }),
        ('Body', {
            'classes': ('collapse-open',),
            'fields': ( 'text', 'html', ),
        }),        
        )
    def action_resend_emails(self, request, queryset):
        for mail in queryset.all():
            mail.send()
    action_resend_emails.short_description = "ADMIN: Re-Send Emails"
    
    def action_send_unsent_emails(self, request, queryset):
        for mail in queryset.all():
            if not mail.sent:
                mail.send()
                self.message_user(request, "Email %s sent." % mail )
    action_send_unsent_emails.short_description = "Send Emails if not sent"

admin.site.register( Email, EmailAdmin )
admin.site.register( MailRecipient )
admin.site.register( MailAttachement )
admin.site.register( MailAttachementFilepath )
admin.site.register( MailHeader )
