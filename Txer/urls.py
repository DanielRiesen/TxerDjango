from django.urls import path, include
from . import views


urlpatterns = [
    path('googleAuth/', views.GoogleAuth.as_view(), name='google-auth'),
    path('googleToken/', views.GoogleToken.as_view(), name='google-token'),
    path('userDetials/', views.GetUserInfo.as_view(), name='user-details'),
    path('userDefault/', views.GetUserDefault.as_view(), name='user-default'),
    path('profile/', views.Profile.as_view(), name='Profile'),

]