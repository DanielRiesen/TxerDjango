import google.oauth2.credentials
from googleapiclient.discovery import build
import google.oauth2.credentials


def build_classroom_api(cred_model):
    credentials = google.oauth2.credentials.Credentials(
        **cred_model.login())
    classroom = build('classroom', 'v1', credentials=credentials)
    return classroom
