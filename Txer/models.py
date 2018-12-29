from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=255, default="Nah")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(null=True, blank=True, max_length=255)
    bio = models.CharField(blank=True, null=True, max_length=255)
    student_id = models.CharField(max_length=255, blank=True, null=True)
    teacher = models.BooleanField(default=False)
    school_code = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class UserFlow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(blank=True, null=True, max_length=60)

    def __str__(self):
        return 'Flow for: ' + self.user.get_full_name()


class CredentialModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(blank=True, null=True, max_length=95, unique=True)
    refresh_token = models.CharField(blank=True, null=True, max_length=95)
    token_uri = models.CharField(blank=True, null=True, max_length=95)
    client_id = models.CharField(blank=True, null=True, max_length=95)
    client_secret = models.CharField(blank=True, null=True, max_length=95)

    def login(self):
        return {'token': self.token,
                'refresh_token': self.refresh_token,
                'token_uri': self.token_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scopes': {'https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/classroom.profile.photos', 'https://www.googleapis.com/auth/classroom.courses.readonly', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/classroom.coursework.students', 'https://www.googleapis.com/auth/classroom.rosters', 'https://www.googleapis.com/auth/classroom.announcements'}}


    def __str__(self):
        return 'Cred Model: '+self.user.get_full_name()
