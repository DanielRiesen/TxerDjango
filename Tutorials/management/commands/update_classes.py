from Tutorials.Shortcuts.shortcuts import register_or_update_class, get_teacher_list, get_student_list
from TxerAPI.Shortcuts.shortcuts import build_classroom_api
from Txer.models import UserProfile
from Tutorials.models import Classes
from django.core.management.base import BaseCommand
from Txer.models import CredentialModel
import time


class Command(BaseCommand):
    help = "Updates all the classes in the database"

    def handle(self, *args, **options):
        start = time.time()
        active_classes = Classes.objects.filter(archived=False)
        classes = [cur for cur in active_classes]
        for cur_class in classes:
            print(cur_class.class_id)
            api = build_classroom_api(CredentialModel.objects.get(user=cur_class.teacher.all().first().user))
            student_list = get_student_list(api.courses().students().list(courseId=cur_class.class_id).execute(), UserProfile)
            teacher_list = get_teacher_list(api.courses().teachers().list(courseId=cur_class.class_id).execute(), UserProfile)
            url = api.courses().get(id=cur_class.class_id).execute()['alternateLink']
            name = api.courses().get(id=cur_class.class_id).execute()['name']
            register_or_update_class(teacher_list, student_list, cur_class.class_id, url, name)
        print("Took {} seconds to update Classes".format(time.time()-start))
