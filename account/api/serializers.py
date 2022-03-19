from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import fields
from account.models import Profile
from rest_framework import serializers, validators
from account.utils import is_image_aspect_ratio_valid, is_image_size_valid
IMAGE_SIZE_MAX_BYTES = 1024 * 100 #100kb
from rest_framework import exceptions
from post.models import Post


import os
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name", "password2", "is_superuser", "is_active","is_staff")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }

    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        is_superuser = self.validated_data['is_superuser']
        is_active = self.validated_data['is_active']
        is_staff = self.validated_data['is_staff']

        if not username.isalnum():
            raise serializers.ValidationError({'username':'Username should only contain alphanumeric characters'})

        if password != password2:
            raise serializers.ValidationError({'password':'Password does not match'})

        account = User(
            username=username,
            email=email ,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser
        )

        account.set_password(password)
        account.save()
        return account

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_superuser=validated_data["is_superuser"],
            is_staff=validated_data["is_staff"],
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["id", "user", "photo_pict"]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "photo_pict"]

    def validate(self, profils):
        try:
            image = profils["photo_pict"]

            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            if image is None:
                return profils

            with storage.open("", "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                os.remove(url)
                raise serializers.ValidationError(
                    {
                        "detail": "That image is too large. Images must be less than 100 kB. Try a different image."
                    }
                )

            if not is_image_aspect_ratio_valid(url):
                os.remove(url)
                raise serializers.ValidationError(
                    {"detail": "Image ratio must be square. Try a different image."}
                )

            os.remove(url)
        except KeyError:
            pass
        return profils


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("password", "first_name", "last_name")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def validates(self,validated_data):
        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]

        account = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        return account