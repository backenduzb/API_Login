from rest_framework import serializers
from .models import User, CustomToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number', 'password']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone_number')
        password = data.get('password')

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            raise AuthenticationFailed({'message': 'Telefon raqami noto‘g‘ri.'})

        if not check_password(password, user.password):
            raise AuthenticationFailed({'message': 'Parol noto‘g‘ri.'})

        data['user'] = user
        return data 