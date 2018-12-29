from Tutorials.models import *
from Txer.models import *
from TxerAPI.Shortcuts.shortcuts import *
from .Announcment import *
import pickle
import os.path
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.common import AzureMissingResourceHttpError
from TxerAPI.settings import azure_storage_key, azure_storage_name
import tempfile


class TutorialProcess(threading.Thread):

    def __init__(self, class_id, thread_id, debug=False, logged=False, max_threads=2, force_update=False):
        threading.Thread.__init__(self)
        self.cred_container = "googleapis"
        self.threadID = thread_id
        self.force_update = force_update
        print(self.force_update)
        self.start_time = time.time()
        self.update_time = datetime.datetime.now()
        self.end_time = time.time()
        self.max_threads = max_threads
        self.class_id = class_id
        # Debug information
        self.debug = debug
        self.errors = 0
        self.logged = logged
        self.query_time = 0
        self.run_time = 0
        self.anc_time = 0
        self.to_save = []
        self.announcement_start = 0
        self.announcement_end = 0
        cred = self.test_cred()  # Tests to see if the credentials are in storage then laod them
        self.flag = True

        if cred:
            self.api = cred
            self.classes = Classes.objects.get(class_id=self.class_id)

        elif not cred:
            self.query_time = time.time()
            self.classes = Classes.objects.get(class_id=self.class_id)
            self.class_cred = CredentialModel.objects.get(user=self.classes.teacher.first().user)
            self.query_time = (time.time() - self.query_time)
            self.api = build_classroom_api(self.class_cred)  # Build API for class
            self.save_cred()

        self.announcements = list(filter(self.filter_api_call,
                                         self.api.courses().announcements().list(courseId=self.class_id).execute()[
                                             'announcements']))

        if len(list(self.announcements)) < 1 and not self.force_update:
            self.flag = False
        else:
            self.flag = True

        if self.flag:
            self.students = [student for student in self.classes.students.all()]
            self.class_teachers = [teacher.user for teacher in self.classes.teacher.all()]
            self.query_time = (
                                      time.time() - self.query_time) / 4  # Calc mean query time... Replace 4 with number of query

        self.run()

    def __str__(self):

        return "Tutorial Process: {}".format(self.threadID)

    def test_cred(self):
        start_time = time.time()
        if os.path.isfile(''.join(self.class_id)):
            to_load = open(''.join(self.class_id), 'rb')
            if self.debug:
                print("Took {} to get API".format(time.time() - start_time))
            cred = pickle.load(to_load)
            return cred
        else:
            return False

    def save_cred(self):
        if self.debug:
            print("saving cred")
        to_save = open(''.join(self.class_id), 'wb')
        pickle.dump(self.api, to_save)
        to_save.close()

    def write_db(self, to_save):

        for data in to_save:
            if data == None:
                pass
            teacher = data['teachers']
            student = data['students']
            del data['teachers']
            del data['students']
            del data['classes']
            instance, created = Tutorial.objects.get_or_create(**data)
            if teacher:
                instance.teacher.add(*[UserProfile.objects.get(user=x) for x in teacher])
            if student:
                if len(student) < 2:
                    student = [student]
                instance.students.set(*student)
            instance.classes.set([self.classes])
            instance.save()

        self.classes.last_updated = self.update_time
        self.classes.save()

    def filter_api_call(self, data):

        start_time = time.time()
        if self.force_update:
            return True

        else:
            data = data['updateTime']
            data = data.split('T')[0] + ' ' + data.split('T')[1]
            data = data[:-1]
            data = data.split('.')[0]
            if (datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=7)) >= (
                    self.classes.last_updated):
                self.flag = True
                if self.debug:
                    print("Took {} to filter request".format(time.time() - start_time))
                return True
            else:
                return False

    def run(self):

        if self.debug:
            print("ANNOUNCEMENTS(S) CAME THROUGH")
        threads = []
        self.announcement_start = time.time()
        for announcement in self.announcements:
            process = AnnouncementProcess(0, announcement, self.students, self.class_teachers, self.classes)
            process.run()
            announcement_processed = process.finished
            try:
                announcement_processed['tutorial_id'] = announcement['id']
                self.to_save.append(announcement_processed)
            except TypeError:
                pass
        self.announcement_end = time.time()
        try:
            self.anc_time = (self.announcement_end - self.announcement_start) / len(list(self.announcements))
        except ZeroDivisionError:
            self.anc_time = 0
        self.write_db(self.to_save)

        self.end_time = time.time()

    def handel_error(self, error_name: str, error_code: int, error_desc: str):
        # Used to print an error during thread and log it
        if self.debug:
            print("_" * 10 + "\n")
            print("UPDATE TUTORIAL RAN INTO AN ERROR")
            print("Error: " + str(error_code) + ", " + error_name + ":")
            print(error_desc)
            print("_" * 10)

        self.errors += 1

    def time_process(self):

        print("_" * 10 + "\n")

        print("MEAN QUERY TIME: " + str(self.query_time) + " seconds")
        print("MEAN ANNOUNCEMENT TIME: " + str(self.anc_time) + " seconds")
        print("TOTAL TIME: " + str(self.end_time - self.start_time) + " seconds")

        print("_" * 10)
