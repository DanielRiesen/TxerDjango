import datetime
import random
import string
import os

from django.db import models
from rest_framework.authtoken.models import Token

from Txer.models import UserProfile

path = os.path.dirname(os.path.realpath(__file__))

def id_gen(size=6, chars=string.ascii_uppercase + string.digits):
    cur = "".join(random.choice(chars) for _ in range(size))
    return cur


class School(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    uuid = models.CharField(primary_key=True, default=id_gen(), max_length=6)
    teacher_code = models.CharField(default=id_gen(), max_length=6)
    location = models.CharField(max_length=90, blank=True, null=True)
    teachers = models.ManyToManyField(UserProfile, related_name='School_Teachers')
    students = models.ManyToManyField(UserProfile, related_name='School_Students')


class Classes(models.Model):
    teacher = models.ManyToManyField(UserProfile, related_name='Class_Teacher')
    teacher_name = models.CharField(default="Not Set", max_length=90)
    class_id = models.CharField(blank=True, null=True, max_length=90)
    students = models.ManyToManyField(UserProfile, related_name='Class_Students')
    archived = models.BooleanField(default=False)
    url = models.URLField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=90)
    school = models.ManyToManyField(School, related_name="Classes_School")
    last_updated = models.DateTimeField(default=datetime.datetime(1000, 1, 1, 1, 1, 1))
    api_built = models.FileField(upload_to="API_Storage/", blank=True, null=True)

    def __str__(self):
        return 'Class: ' + self.class_id

    def list_students(self):
        return self.students.objects.all()


class Tutorial(models.Model):
    teacher = models.ManyToManyField(UserProfile, related_name='Tutorial_Teacher')
    students = models.ManyToManyField(UserProfile, related_name='Tutorial_Students')
    classes = models.ManyToManyField(Classes, related_name='Tutorial_Class')
    mandatory = models.BooleanField(default=False)
    MinStudent = models.IntegerField(default=0)
    MaxStudent = models.IntegerField(default=10000)
    Joinable = models.BooleanField(default=False)
    Desc = models.CharField(max_length=90, blank=True, null=True)
    Start_Time = models.DateTimeField(blank=True, null=True)
    End_Time = models.DateTimeField(blank=True, null=True)
    Location = models.CharField(max_length=90, default="Not Set")
    tutorial_id = models.CharField(max_length=90, blank=True, null=True)
    attended_students = models.ManyToManyField(UserProfile, related_name='Attended_students')
    tutorial_material = models.FileField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    repeat_weekly = models.BooleanField(blank=True, null=True)
    repeat_daily = models.BooleanField(blank=True, null=True)
    repeat_monday = models.BooleanField(blank=True, null=True)
    repeat_tuesday = models.BooleanField(blank=True, null=True)
    repeat_wednesday = models.BooleanField(blank=True, null=True)
    repeat_thursday = models.BooleanField(blank=True, null=True)
    repeat_friday = models.BooleanField(blank=True, null=True)
    repeat_saturday = models.BooleanField(blank=True, null=True)
    repeat_sunday = models.BooleanField(blank=True, null=True)
    repeat_start_date = models.DateField(blank=True, null=True)
    repeat_end_date = models.DateField(blank=True, null=True)

    def __str__(self):

        if not self.tutorial_id:
            return 'Tutorial: Undefined ID'

        return 'Tutorial: ' + self.tutorial_id

    def create_from_request(self, data):

        self.tutorial_id = random.randint(0,10000)

        self.save()

        del data['csrfmiddlewaretoken']

        for stu in data['students']:
            self.students.add(UserProfile.objects.get(student_id=stu))

        print(data['teachers'][0])
        self.teacher.add(UserProfile.objects.get(user=Token.objects.get(key=data['teachers'][0]).user))

        for cur_course in data['course']:
            self.classes.add(Classes.objects.get(class_id=cur_course))

        if data['mandatory']:
            self.mandatory = True

        if data['joinable']:
            self.Joinable = True

        self.MinStudent = data['min_students'][0]
        self.MaxStudent = data['max_students'][0]
        self.Desc = data['desc'][0]
        self.Location = data['location'][0]
        date_split = data['date'][0].split('/')
        start_time_split = data['start_time'][0].split(':')
        end_time_split = data['end_time'][0].split(':')
        self.Start_Time = '{}-{}-{} {}:{}'.format(date_split[0], date_split[2], date_split[1],
                                                  start_time_split[0], start_time_split[1])
        self.End_Time = '{}-{}-{} {}:{}'.format(date_split[0], date_split[2], date_split[1],
                                                end_time_split[0], end_time_split[1])

        self.save()
