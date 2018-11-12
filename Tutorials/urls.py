from django.urls import path, include
from . import views


urlpatterns = [
    path('courses/', views.Courses.as_view(), name='course-view'),
    path('schools/', views.Schools.as_view(), name='school-list'),
    path('googleCourses/', views.GoogleCourses.as_view(), name='GoogleCourses'),
]