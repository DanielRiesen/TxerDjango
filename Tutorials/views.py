from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Classes
from Txer.models import UserProfile

class Courses(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pass

    def get(self, request):
        query = Classes.objects.filter(teacher=UserProfile.objects.get(user=request.user))
        serilizer_class = Course(query)
        return Response(serilizer_class.data)

    def delete(self, reqeust):
        pass