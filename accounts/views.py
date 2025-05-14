from django.shortcuts import render
from .models import CustomToken,User
from .serializers import UserSerializer,UserLoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


class CreateUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        token, created = CustomToken.objects.get_or_create(
            user=user,
        )
        return Response({'token': token.key, "message": "Login successful"}, status=status.HTTP_200_OK)
