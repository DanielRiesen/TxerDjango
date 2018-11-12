from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from TxerAPI.Shortcuts import shortcuts
from .Shortcuts.shortcuts import *


# View to manage already registered classes in the database
class Courses(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        query = Classes.objects.filter(students=UserProfile.objects.get(user=request.user))
        serilizer_class = Course(query, many=True)
        print(serilizer_class.data)
        return Response(serilizer_class.dataa)


# View to manage Schools
class Schools(APIView):

    @staticmethod
    def post(request):
        School.objects.get_or_create(**request.data)
        return Response(status=status.HTTP_201_CREATED)


# View to retrieve google classroom classes and to register them
class GoogleCourses(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        classroom = shortcuts.build_classroom_api(CredentialModel.objects.get(user=request.user))
        courses_listed = classroom.courses().list().execute()
        print(courses_listed)
        return Response(data=courses_listed)

    @staticmethod
    def post(request):
        for cur_class in request.data['courses']:
            classroom = shortcuts.build_classroom_api(CredentialModel.objects.get(user=request.user))
            student_list = get_student_list(classroom.courses().students().list(courseId=cur_class).execute(),
                                            UserProfile)
            teacher_list = get_teacher_list(classroom.courses().teachers().list(courseId=cur_class).execute(),
                                            UserProfile)
            print("teacher_list: " + str(teacher_list))
            print("student_list:" + str(student_list))
            url = classroom.courses().get(id=cur_class).execute()['alternateLink']
            name = classroom.courses().get(id=cur_class).execute()['name']
            register_or_update_class(teacher_list, student_list, cur_class, url, name)
        return Response(status=status.HTTP_201_CREATED)


