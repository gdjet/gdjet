# -*- coding: utf-8 -*-
from gdjet.permy.groups import *
from gdjet.permy.permissions import *
from gdjet import settings

def create_manager_group(**kwargs):
    from gdjet.models.manager import ManagerModule
    g = create_group( "ManagerTestGroup", [ permission_add(ManagerModule), ] )


def setup_manager(**kwargs):
    """
        An example how you could register global options to gdjet.manager.
        
    """
    try:
        from gdjet.manager import register_url, register_module, register_option, register_string
        register_module( name = "manager",
                         label = "Manager Setup",
                         enabled = True,
                         restricted = False,
                         prefix = getattr(  
                            getattr( settings, 'PREFIX', {'MANAGER': '/manager/'} ),
                                                'MANAGER', '/manager/' ),
                         description = """
                         This module controls the Management Console.
                         It is responsible for managing all the sites' plugins
                         """ )
        register_url(
                          mname = "manager",
                          name = "listplugins",
                          label = "List of Plugins",
                          sidebar = True,
                          url = "/listplugins",
                          )
        register_option( 
                        mname = 'manager',
                        name = 'dummy_option',
                        label = 'A Dummy Option to test it',
                        enabled = True,
                        )
        register_string(mname = 'manager',
                        name = 'manager_base_template',
                        label = 'BaseTemplate to use for manager',
                        value = '/gdjet/manager/design.html'
                        )
    except Exception, e:
        import sys
        sys.stderr.write( "Error while registering with gdjet.manager: %s" % e )


if settings.MODULE_TEST:
    from django.db.models.signals import post_syncdb
    from gdjet import models
    post_syncdb.connect(setup_manager, sender=models)
    post_syncdb.connect(create_manager_group, sender=models)
