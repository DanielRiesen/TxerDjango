from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from Txer.models import *


class Course(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = Classes
        fields = ('name', 'url', 'teacher_name')


class SchoolSer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('name','uuid')


class TeacherSer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('username',)


class TutorialSer(serializers.ModelSerializer):

    class Meta:
        depth = 2
        model = Tutorial
        fields = ("teacher", "Desc", "tutorial_id", "mandatory", "classes", "Start_Time", "End_Time", "Location")
