from django.core.management.base import BaseCommand
from Tutorials.Shortcuts.shortcuts import *
from Tutorials.models import *
from datetime import *
import time
import threading

class myThread(threading.Thread):
   def __init__(self, threadID, name, cur_class, cred):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.cur_class = cur_class
      self.cred = cred
      self.name = name
   def run(self):
       print("Starting Thread: "+str(self.threadID))
       check_announcements_and_update([self.cur_class.class_id], self.cred)
       print('finished update')
       for tut in Tutorial.objects.filter(Start_Time__isnull=True):
           tut.archived = True
           tut.save()

       for tut in Tutorial.objects.filter(archived=False).filter(End_Time__lte=datetime.now() - timedelta(days=-1)):
           tut.archived = True
           tut.save()


class Command(BaseCommand):

    help = "Check all registered classes and update their upcoming tutorials and archives any which date, or repeat " \
           "date, has passed."

    def handle(self, *args, **options):
        threads = []
        start = time.time()

        errors = 0
        active_classes = Classes.objects.filter(archived=False)
        classes_with_cred = {}
        for cur in active_classes:
            try:
                classes_with_cred[cur] = CredentialModel.objects.get(user=cur.teacher.all()[0].user)
            except IndexError:
                pass
        for cur_class, cred in classes_with_cred.items():
            threads.append(myThread(1, "Thread-1", cur_class, cred))

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        end = time.time()
        print(end - start)