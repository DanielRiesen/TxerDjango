from django.core.management.base import BaseCommand
from Tutorials.tutorial_updater.Tutorial import *
import pickle


class Command(BaseCommand):
    help = "Check all registered classes and update their upcoming tutorials and archives any which date, or repeat " \
           "date, has passed."

    def add_arguments(self, parser):
        parser.add_argument('threads', nargs='+', type=int)
        parser.add_argument(
            '--full',
            action='store_true',
            dest='full_update',
            help='Full refresh of the database no matter the date',
        )
        parser.add_argument(
            '--repeat',
            action='store_true',
            dest='repeat',
            help='Infinite Loop of Updates',
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            help='Print Debug options',
        )

    def handle(self, *args, **options):

        Flag = True

        while Flag:
            cur = 0
            threads = []
            start_time = time.time()
            while len(Classes.objects.all()) > cur:
                if cur + options['threads'][0] < len(Classes.objects.all()):
                    for x in range(options['threads'][0]):
                        threads.append(
                            TutorialProcess(Classes.objects.all()[cur + x].class_id, x,
                                            force_update=options['full_update'], debug=options['debug']))
                else:
                    for x in range(len(Classes.objects.all()) - options['threads'][0], len(Classes.objects.all())):
                        if x < 0:
                            pass
                        else:
                            threads.append(
                                TutorialProcess(Classes.objects.all()[x].class_id, x,
                                                force_update=options['full_update'], debug=options['debug']))
                [thread.start() for thread in threads]
                print(len(threads))

                cur += options['threads'][0]
            end_time = time.time()
            if not options['repeat']:
                Flag = False
            else:
                print(end_time - start_time)
