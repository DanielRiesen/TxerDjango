from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CredSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CredentialModel
        fields =  ('token', 'refresh_token', 'token_uri', 'client_id', 'client_secret', 'scopes')