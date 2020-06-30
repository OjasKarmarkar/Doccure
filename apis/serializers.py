from rest_framework import serializers
from apis.models import CustomUser
from restroapp.models import Appointment
from django.contrib.auth.hashers import make_password


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','first_name' , 'last_name')
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.age = validated_data.get('age', instance.age)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance



class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'city', 'state','profession')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
    def create(self, validated_data):
        return Appointment.objects.create(**validated_data)