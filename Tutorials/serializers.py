from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class Course(serializers.HyperlinkedModelSerializer):

    class Meta:

        model = Classes
        fields = ('name', 'url', 'teacher_name')


class SchoolSer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ('name','uuid')
