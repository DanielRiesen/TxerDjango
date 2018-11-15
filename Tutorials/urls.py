from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.Courses.as_view(), name='course-view'),
    path('schools/', views.Schools.as_view(), name='school-list'),
    path('tutorials/', views.Tutorials.as_view(), name='tutorials-list'),
    path('googleCourses/', views.GoogleCourses.as_view(), name='GoogleCourses'),
]
