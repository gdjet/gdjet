# -*- coding: utf-8 -*-
from gdjet.forms.registration import RegistrationFormBase

def post_registration( regform, user, code ):
    """
        happens after registration is done.
        you might want to create a profile or something.
        the user has been saved to django already.
        if you return a HttpResponse it will be shown.
        
        regform contains the Form's cleaned_data!!
    """
    # you can use send_mail from here:
    # from gdjet.registration import email
    # email.send_email( user, code )
    return user

def post_validation( regobj, user ):
    """
        happens after validation code has been found.
        if you return a HttpResponse it will be shown.
        so you can create the userprofile after validation.
        note: user is set active in this function.
        don't you forget!
        
        regobj contains a Registration object.
    """
    regobj.validated = True
    regobj.validation_code= '!'
    user.is_active = True
    regobj.save()
    user.save()
    return user

def invalid_validation( request, what ):
    """
        This Validation was invalid, either because:
            * user put in was invalid (nonexistant)
            * code put in was invalid (not present, OR wrong user)
        You can return a HttpResponse.
    """
    # what can be: code, user
    # return can be a HttpResponse. Like a 404.
    # you might want to log this and block IPs.
    return None

# override this with YOUR registrationform.
RegistrationForm = RegistrationFormBase 
