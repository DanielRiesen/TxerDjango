from django.core.management.base import BaseCommand
from Tutorials.Shortcuts.shortcuts import *
from Tutorials.models import *


class Command(BaseCommand):
    help = 'Checks all linked classes and updates their tutorial fields'

    def handle(self, *args, **options):
        errors = 0
        active_classes = Classes.objects.filter(archived=False)
        classes_with_cred = {cur: CredentialModel.objects.get(user = cur.teacher.all()[0].user) for cur in active_classes}
        for cur_class, cred in classes_with_cred.items():
            check_announcements_and_update([cur_class.class_id], cred)
            print('check')
        self.stdout.write(self.style.SUCCESS('Success!'))
        self.stdout.write(self.style.SUCCESS('Number Of Errors: '+ str(errors)))
