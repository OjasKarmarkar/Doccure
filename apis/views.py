from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from apis.serializers import CurrentUserSerializer , AppointmentSerializer
from .models import CustomUser
from restroapp.models import Appointment


# Create your views here.


class UserLoginView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:
           #print(request.user.username)
           content = {'email': request.user.email}
           return Response(content)
        else:
           content = {'message': 'User Not Authenticated'}
           return Response(content)

class DoctorDashboard(APIView):
    def post(self, request):
      userEmail = request.data['email']
      print(userEmail)
      try:
        user = CustomUser.objects.get(email=userEmail)
      except CustomUser.DoesNotExist:
        user = None
      appointmentList = Appointment.objects.filter(doctorMail = userEmail)
      serializer = AppointmentSerializer(appointmentList , many=True)
      serializer.data
      content = {'Appointments': serializer.data}
      return Response(content)
class UserRegisterView(APIView):
    def post(self, request):
      serializer = CurrentUserSerializer(data = request.data)
      if serializer.is_valid():
          serializer.save()
          content = {'message': 'User Created Succesfully'}
          return Response(content)
      else:
         content = {'message': serializer.errors}
         return Response(content)
     
