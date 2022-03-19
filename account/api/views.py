from django.contrib.auth.models import User
from django.http import response
from account.models import Profile
from .serializers import AccountSerializer, ProfileSerializer, ProfileUpdateSerializer, RegisterSerializer, UserSerializer, UserUpdateSerializer
from urllib import request
from account.renderers import MyRenderer

from knox.auth import AuthToken

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

#PROFILE
class UserListRegistration(generics.ListCreateAPIView): 
    authentication_classes = []
    permission_classes = []
    pagination_class = PageNumberPagination
    renderer_classes = [MyRenderer]
    queryset = User.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RegisterSerializer
        return AccountSerializer

def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "password": user.password,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
    }

def serialize_profile(profils):
    return {
        "user": profils.user,
        "photo_pict": profils.photo_pict,
    }

class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [MyRenderer]
    queryset = Profile.objects.all()
    lookup_field = "id"
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProfileUpdateSerializer
        return ProfileSerializer


#USER

@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_data': serialize_user(user),
        'token': token
    })
        

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user_info": serialize_user(user),
            "token": token
        })


@api_view(['GET'])
def get_user(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_data': serialize_user(user)
        })
    return Response({})

# @api_view(['PUT'])
# def change_user(request)
class UserEdit(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [MyRenderer]
    queryset = User.objects.all()
    lookup_field = "id"
    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer
        return UserSerializer