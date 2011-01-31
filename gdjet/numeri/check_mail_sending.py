#! /usr/bin/python
import os
import sys
sys.stdout = sys.stderr
sys.path.insert( 0, '/home/web_denkzettel/applications' )
sys.path.insert( 0, '/home/web_denkzettel/project' )
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from django.core.management import setup_environ
# from project import settings
# setup_environ(settings)

from gdjet.models import Email

for email in Email.objects.all():
   print email.title

