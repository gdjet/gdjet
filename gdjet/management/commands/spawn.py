# -*- coding: utf-8 -*-
"""
    Spawn Command
    
    * Spawn collects all commands from GDJET_SPAWNS setting
    * All commands are executed in a thread
    * A simple control API is running in foreground.
    
    @author g4b
"""
from django.core.management.base import BaseCommand
import sys
from gdjet.utils.threads import ThreadWithExc

class ParallelManageTask(ThreadWithExc):
    def __init__(self, settings, argv, klass ):
        super(self).__init__()
        self.settings=settings
        self.argv=argv
        self.klass=klass

    def run(self):
        #setup_environ(self.settings)
        self.utility = self.klass(self.argv)
        self.utility.execute()
        
    def run_threaded(self):
        self.daemon = True
        self.start()

class Command(BaseCommand):
    help = "Spawns multiple threads with management commands"
    args = ''
    # We do not work with models yet.
    requires_model_validation = False
    def handle(self, *args, **options):
        from gdjet import settings
        spawns = settings.SPAWNS
        for spawn in spawns:
            argv=sys.argv
            if isinstance(spawn, tuple):
                spawn, argv = spawn
            rt=ParallelManageTask(**argv)
            rt.run_threaded()
            self.running_tasks+=[rt]
        try:
            command = None
            while command not in ['exit', 'x']:
                command = raw_input(':)').lower()
                if command=='s' or command=='show':
                    print "Running Tasks: %s" % len(self.running_tasks)
                elif command=='h' or command=='help':
                    print "at the moment only show/s or help/h or exit/x are available commands"    
        except KeyboardInterrupt:
            # send KeyboardInterrupt to all child threads:
            
            # now exit
            sys.exit(0)
        
            