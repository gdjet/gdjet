# -*- coding: utf-8 -*-
"""
    Spawn Command
    
    * Spawn collects all commands from GDJET_SPAWNS setting
    * All commands are executed in a thread
    * A simple control API is running in foreground.
    
    @author g4b
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Spawns multiple threads with management commands"
    args = ''
    # We do not work with models yet.
    requires_model_validation = False
    def handle(self, *args, **options):
        import sys
        from gdjet import settings
        from django.core.management import setup_environ, ManagementUtility
        from gdjet.utils.threads import ThreadWithExc
        from threading import Thread
        class ParallelManageTask(Thread):
            def __init__(self, argv, klass ):
                super(ParallelManageTask, self).__init__()
                self.argv=argv
                self.klass=klass
        
            def run(self):
                self.utility = self.klass(self.argv)
                self.utility.execute()
                
            def run_threaded(self):
                self.daemon = True
                self.start()
        
        spawns = settings.SPAWNS
        self.running_tasks=[]
        
        for spawn in spawns:
            if isinstance(spawn, basestring):
                spawn = [ sys.argv[0], spawn ]
            else:
                spawn.insert(0, sys.argv[0])
            rt=ParallelManageTask( argv=spawn,
                                   klass=ManagementUtility )
            rt.run_threaded()
            self.running_tasks+=[rt]
        try:
            while True:
                command = raw_input(':)')
                command = command.lower()
                if command=='s' or command=='show':
                    print "Running Tasks: %s" % len(self.running_tasks)
                    for task in self.running_tasks:
                        print "%s (%s)" % ( task.name, task.is_alive() )
                elif command=='h' or command=='help':
                    print "help to be written yet"
                elif command=='r' or command=='run':
                    for task in self.running_tasks:
                        if not task.is_alive():
                            print "running task: %s" % task.name
                            task.run_threaded()
                elif command=='x' or command=='exit':
                    # cleanups?
                    print "bye!"
                    sys.exit(0)
        #except KeyboardInterrupt:
        #    # send KeyboardInterrupt to all child threads:
        #    for child in self.running_tasks:
        #        if isinstance(child, ThreadWithExc):
        #            child.raiseExc(KeyboardInterrupt)
        #    # now exit
        #    sys.exit(0)
        except:
            import traceback
            traceback.print_exc()
            raise
            