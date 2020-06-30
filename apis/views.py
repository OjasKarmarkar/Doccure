from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from apis.serializers import CurrentUserSerializer , AppointmentSerializer, SearchSerializer
from .models import CustomUser
from restroapp.models import Appointment
import random
import string
from datetime import datetime


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


class PatientDashboard(APIView):
    def post(self, request):
      userEmail = request.data['email']
      print(userEmail)
      try:
        user = CustomUser.objects.get(email=userEmail)
      except CustomUser.DoesNotExist:
        user = None
      appointmentList = Appointment.objects.filter(patientMail = userEmail)
      serializer = AppointmentSerializer(appointmentList , many=True)
      serializer.data
      content = {'Appointments': serializer.data}
      return Response(content)


class Search(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
      if request.user.is_authenticated:
        user = request.user
        if request.data.get('book', '')!= '':
          try:
            doctor = CustomUser.objects.get(email=request.data.get('book', ''))
          except CustomUser.DoesNotExist:
            doctor = None
          if doctor == None:
            return Response({'status': 'Doctor Not Found!'})
          else:
            ip = request.data.get('doa', '').split('/')
            Appointment.objects.create(appointmentId= self.randomString(), doctorMail= doctor.email,special=doctor.profession, patientMail= user.email, patientName= user.first_name + user.last_name, doctorName= doctor.first_name + doctor.last_name,patientPhoto= user.photo, doctorPhoto= doctor.photo, dateOfAppointment= datetime(int(ip[-1]), int(ip[1]), int(ip[0])), status= "UNREVIEWED")
            return Response({'status':'success'})
        if request.data.get('getspl','') == '1':
          fields = [ x['profession'] for x in CustomUser.objects.values('profession').distinct()]
          content = {'spl': fields}
          return Response(content)
        sName = request.data.get('name', '')
        spl = request.data.get('spl', '')
        #
        if sName != '' and spl != '':
          doctors = CustomUser.objects.filter(is_doc=True, first_name__startswith=sName, profession=spl)
        elif sName != '':
          doctors = CustomUser.objects.filter(is_doc=True, first_name__startswith=sName)
        elif spl != '':
          doctors = CustomUser.objects.filter(is_doc=True, profession=spl)
        else:
          doctors = CustomUser.objects.filter(is_doc=True)
        serializer = SearchSerializer(doctors , many=True)
        content = {'doctors': serializer.data}
        return Response(content)
      else:
        return Response({'status': 'unauthorized'})
    
    def randomString(self, stringLength=8):
      letters = string.ascii_lowercase
      return ''.join(random.choice(letters) for i in range(stringLength))

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
     
