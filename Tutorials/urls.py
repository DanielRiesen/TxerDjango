from django.urls import path
from . import views

urlpatterns = [
    path('courses/<str:num>', views.Courses.as_view(), name='course-view'),
    path('course_details/<str:id>', views.CourseDetails.as_view(), name='course-view'),
    path('teaching_courses/<str:num>', views.TeachingCourses.as_view(), name='teaching-course-view'),
    path('schools/', views.Schools.as_view(), name='school-list'),
    path('schools_details/<str:uuid>', views.Schools.as_view(), name='school-details'),
    path('tutorials/<str:num>', views.Tutorials.as_view(), name='tutorials-list'),
    path('teacher_tutorials/<str:num>', views.TeachingTutorials.as_view(), name='teacher-tutorial-list'),
    path('googleCourses/', views.GoogleCourses.as_view(), name='GoogleCourses'),
]
