from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class Course(serializers.ModelSerializer):

    class Meta:
        model = Classes
        fields = '__all__'