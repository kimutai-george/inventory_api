from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime
from inventory_api.utils import get_access_token
from inventory_api.custom_methods import *
# Create your views here.

def add_user_activities(user,action):
    UserActivities.objects.create(
        user_id=user.id,
        email=user.email,
        fullname=user.fullname,
        action=action
    )

class CreateUserView(ModelViewSet):
    http_methods_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def create(self,request):
        valid_request= self.serializer(data=request.data)
        valid_request.is_valid(raise_exception=True)
        CustomUser.objects.create(**valid_request.validated_data)

        add_user_activities(request.user,"added new user")

        return Response({"success":"user created successfully"},status=status.HTTP_201_CREATED)


class LoginView(ModelViewSet):
    http_methods_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request):
        valid_request = self.serializer(data=request.data)
        valid_request.is_valid(raise_exception=True)

        new_user = valid_request.validated_data["is_new_user"]

        if new_user:
            user = CustomUser.objects.filter(email=valid_request.validated_data["email"])

            if user:
                user = user[0]
                if not user.password:
                    return Response({"user_id":user.id})
                else:
                    raise Exception("user has password already")

            else:
                raise Exception("User with email doesn't exist")

        user = authenticate(
            username = valid_request.validated_data["email"],
            password=valid_request.validated_data("password",None)
        )

        if not user:
            return Response(
                {"error":"invalid username or email"},
                status=status.HTTP_400_BAD_REQUEST
            )
        access = get_access_token({"user_id":user.id},1)

        user.last_login = datetime.now()
        user.save()
        add_user_activities(user, "logged in")
        return Response({"access":access})


class UpdatePasswordView(ModelViewSet):
    http_methods_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = UpdatePasswordSerializer

    def create(self,request):
        valid_request = self.serializer(data=request.data)
        valid_request.is_valid(raise_exception=True)

        user = CustomUser.objects.filter(id=valid_request.validated_data["id"])

        if not user:
            raise Exception("user with id not found")

        user = user[0]
        user.set_password(valid_request.validated_data["password"])
        user.save()
        add_user_activities(user, "updated password")

        return Response({'success':'password updated successfully'})

class MeView(ModelViewSet):
    http_methods_names = ["get"]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def list(self,request):
        data = self.serializer_class(request.user).data
        return Response(data)


class UserActivitiesView(ModelViewSet):
    http_methods_names = ["get"]
    queryset = UserActivities.objects.all()
    serializer_class = UserActivitiesSerializer
    permission_classes = (IsAuthenticatedCustom,)

class UsersView(ModelViewSet):
    http_methods_names = ["get"]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedCustom,)

    def list(self,request):
        users = self.queryset().filter(is_superuser=False)
        data = self.serializer_class(users,many=True).data
        return Response(data)