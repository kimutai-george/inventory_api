from rest_framework import serializers
from .models import *

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname=serializers.CharField()
    role = serializers.ChoiceField(Roles)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False)
    is_new_user = serializers.BooleanField(default=False,required=False)

class UpdatePasswordSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField()

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ["password"]

class UserActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivities
        fields = ("__all__")