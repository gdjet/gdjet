# -*- coding: utf-8 -*-
from django import forms
from django.forms import widgets

class LoginForm( forms.Form ):
    username = forms.CharField( label = u'Username', max_length=75, min_length=1 )
    password = forms.CharField( label = u'Passwort', widget = widgets.PasswordInput )
    
