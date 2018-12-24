from Tutorials.models import *
from Txer.models import *

class TutorialProcess:

    def __init__(self, class_id, max_threads=2):

        self.max_threads = max_threads
        self.class_id = class_id

        # Now we gather all the data we need from the database to make sure we don't waste calls

        self.classes = Classes.objects.get(class_id=self.class_id)
        self.class_teachers = [teacher.UserProfile for teacher in self.classes.teacher.all()]
        self.class_cred = CredentialModel.objects.get(user=self.class_teachers[0].user)
        self.students = [student.UserProfile for student in self.classes.students]

    def run(self):
        print(self.max_threads)
        print(self.class_id)
        print(self.classes)
        print(self.class_teachers)
        print(self.class_cred)
        print(self.students)
