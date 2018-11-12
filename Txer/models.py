from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/profile_pictures',
                                      default='/profiles/profile_pictures/default.svg')
    bio = models.CharField(blank=True, null=True, max_length=200)
    student_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return 'Profile: '+self.user.get_full_name() + ' ' + self.student_id


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
