from rest_framework import serializers
from apis.models import CustomUser
from restroapp.models import Appointment
from django.contrib.auth.hashers import make_password


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password' , 'first_name' , 'last_name')
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
    def create(self, validated_data):
        return Appointment.objects.create(**validated_data)