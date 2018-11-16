from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    username = models.CharField(max_length=40, default="Nah")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(null=True, blank=True, max_length=200)
    bio = models.CharField(blank=True, null=True, max_length=200)
    student_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class UserFlow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(blank=True, null=True, max_length=300)

    def __str__(self):
        return 'Flow for: ' + self.user.get_full_name()


class CredentialModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(blank=True, null=True, max_length=300, unique=True)
    refresh_token = models.CharField(blank=True, null=True, max_length=300)
    token_uri = models.CharField(blank=True, null=True, max_length=300)
    client_id = models.CharField(blank=True, null=True, max_length=300)
    client_secret = models.CharField(blank=True, null=True, max_length=300)
    scopes = models.CharField(blank=True, null=True, max_length=300)

    def login(self):
        return {'token': self.token,
                'refresh_token': self.refresh_token,
                'token_uri': self.token_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scopes': self.scopes}


    def __str__(self):
        return 'Cred Model: '+self.user.get_full_name()
