from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from TxerAPI.Shortcuts import shortcuts
from .Shortcuts.shortcuts import *
from datetime import *


# View to manage already registered classes in the database
class Courses(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, num):
        query = Classes.objects.filter(students=UserProfile.objects.get(user=request.user))[:int(num)]
        serilizer_class = Course(query, many=True)
        print(serilizer_class.data)
        for x in serilizer_class.data:
            if len(x['teacher']) > 1:
                x['teacher'] = x['teacher'][0]
        return Response(serilizer_class.data)


class CourseDetails(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, id):
        query = Classes.objects.get(class_id=int(id))
        print(id)
        serilizer_class = CourseDetailsSer(query)
        print(serilizer_class.data)
        return Response(serilizer_class.data)


class TeachingCourses(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, num):
        query = Classes.objects.filter(teacher=UserProfile.objects.get(user=request.user))[:int(num)]
        serilizer_class = Course(query, many=True)
        print(serilizer_class.data)
        return Response(serilizer_class.data)


# View to manage Schools
class Schools(APIView):

    @staticmethod
    def post(request):
        print(request.data)
        school, created = School.objects.get_or_create(name=request.data['name'], location=request.data['location'])
        return Response(status=status.HTTP_201_CREATED, data=school.uuid)

    @staticmethod
    def get(request, uuid):
        serializer = SchoolSer(query=School.objects.get(uuid=uuid))
        return Response(status=status.HTTP_202_ACCEPTED, data=serializer.data)


# View to retrieve google classroom classes and to register them
# You can only register courses that you own.
class GoogleCourses(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        classroom = shortcuts.build_classroom_api(CredentialModel.objects.get(user=request.user))
        courses_listed = classroom.courses().list().execute()
        courses_teaching = {'courses':[]}
        print(courses_listed['courses'][0]['ownerId'])
        for x in courses_listed['courses']:
            if x['ownerId'] == UserProfile.objects.get(user=request.user).student_id:
                courses_teaching['courses'].append(x)
        print(courses_teaching)
        return Response(data=courses_teaching)

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


class Tutorials(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, num):
        query = Tutorial.objects.filter(students=UserProfile.objects.get(user=request.user))
        query = query.filter(Start_Time__isnull=False)
        query = query.order_by('Start_Time')[0:int(num)]
        serilizer_class = TutorialSer(query, many=True)
        return Response(status=status.HTTP_202_ACCEPTED, data=serilizer_class.data)


class TeachingTutorials(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, num):
        query = Tutorial.objects.filter(teacher=UserProfile.objects.get(user=request.user))
        query = query.filter(Start_Time__isnull=False)
        query = query.filter(Start_Time__gte=datetime.now()-timedelta(hours=1))
        query = query.order_by('Start_Time')[0:int(num)]
        serilizer_class = TutorialSer(query, many=True)
        return Response(status=status.HTTP_202_ACCEPTED, data=serilizer_class.data)