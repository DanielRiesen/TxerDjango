from multiprocessing.dummy import Pool as ThreadPool

from django.core.management.base import BaseCommand

from Tutorials.tutorial_updater.Tutorial import *


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

        start_time = time.time()
        class_list = list(Classes.objects.all())
        print(options['full_update'])
        if options['debug']:
            print(class_list)

        def update_tutorial(classes):
            TutorialProcess(classes.class_id, classes.class_id, force_update=options['full_update'], debug=options['debug'])

        pool = ThreadPool(int(options['threads'][0]))
        results = pool.map(update_tutorial, class_list)
        pool.close()
        pool.join()
        if options['debug']:
            print(time.time()-start_time)