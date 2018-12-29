import os
import random

from google.auth.transport import requests
from google.oauth2 import id_token
from oauth2client import client
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Tutorials.models import School
from TxerAPI import settings
from TxerAPI.Shortcuts.shortcuts import build_classroom_api
from .serializers import *


class GoogleAuth(APIView):

    @staticmethod
    def post(request):

        idinfo = id_token.verify_oauth2_token(request.data['Zi']['id_token'], requests.Request(), "962650220393-o5upillndnmij30pdsgktb58fnmm3b4o.apps.googleusercontent.com")
        userid = idinfo['sub']
        account, created = User.objects.get_or_create(email=idinfo['email'])
        token, _ = Token.objects.get_or_create(user=account)
        token = token.key
        print(created)
        return Response(data={'token': token, 'created': created})


class GoogleToken(APIView):

    serializers = CredSerializer()

    @staticmethod
    def post(request):

        credentials = client.credentials_from_clientsecrets_and_code(
            os.path.join(settings.BASE_DIR, 'Tutorials', 'secret_file.json'),
            [
             'https://www.googleapis.com/auth/calendar',
             'https://www.googleapis.com/auth/classroom.courses.readonly',
             'https://www.googleapis.com/auth/classroom.profile.photos',
             'https://www.googleapis.com/auth/classroom.announcements',
             'https://www.googleapis.com/auth/classroom.coursework.students',
             'https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile',
             'https://www.googleapis.com/auth/classroom.rosters'],
            request.data['code'])
        account, created = User.objects.get_or_create(email=credentials.id_token['email'], username=credentials.id_token['email'])
        account.username = account.id
        token, created = Token.objects.get_or_create(user=account)
        token = token.key
        cred, _ = CredentialModel.objects.get_or_create(user=account)
        cred.token = credentials.refresh_token
        cred.refresh_token = credentials.refresh_token
        cred.token_uri = credentials.token_uri
        cred.client_id = credentials.client_id
        cred.client_secret = credentials.client_secret
        cred.save()

        return Response({'token': token, 'created': created}, status=status.HTTP_202_ACCEPTED)


class GetUserInfo(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        query = UserProfile.objects.get(user=request.user)
        serializer_class = ProfileSerializer(query)
        print(serializer_class.data)
        return Response(serializer_class.data)


class PublicProfile(APIView):

    @staticmethod
    def get(request, id):
        print(id)
        query = UserProfile.objects.get(pk=int(id))
        serializer_class = ProfileSerializer(query)
        return Response(serializer_class.data)


class GetUserDefault(APIView):

    @staticmethod
    def get():
        return Response(data={'username': 'anon', 'email': 'anon', 'password': 'anon'})


class Profile(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        classroom = build_classroom_api(CredentialModel.objects.get(user=request.user))
        print(classroom)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.username = request.data['username']
        profile.bio = request.data['desc']
        google_data = classroom.userProfiles().get(userId='me').execute()
        profile.profile_image = google_data['photoUrl']
        print(google_data)
        profile.student_id = google_data['id']
        print(request.data)
        profile.school_code = request.data['school']
        try:
            school = School.objects.get(uuid=request.data['school'])
            school.students.add(profile)
            user_type = "student"
        except School.DoesNotExist:
            try:
                school = School.objects.get(teacher_code=request.data['school'])
                school.teachers.add(profile)
                user_type = "teacher"
                profile.teacher = True
            except School.DoesNotExist:
                profile.school_code = ''
                return Response(status=status.HTTP_400_BAD_REQUEST)
        profile.save()
        school.save()
        return Response(status=status.HTTP_201_CREATED, data={"user_type":user_type})

