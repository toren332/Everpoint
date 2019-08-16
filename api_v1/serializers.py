from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import password_validation
from service import models


class LatLngHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LatLngHistory
        exclude = ['id']


class ShipSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ship
        fields = '__all__'




class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(max_length=128, required=True)

    @staticmethod
    def validate_password(password: str) -> str:
        password_validation.validate_password(password)
        return password

    @staticmethod
    def validate_username(username: str) -> str:
        if User.objects.filter(username=username).exists():
            msg = 'Someone already has account with this username'
            raise serializers.ValidationError(msg)
        return username

    def create(self, validated_data: dict) -> [User, int, dict]:
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate(self, data: dict) -> dict:
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            error_msg = 'The username / email or password is not correct'
            raise serializers.ValidationError(error_msg)

        return data
