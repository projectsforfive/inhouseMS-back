from django.shortcuts import render
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import authenticate

from .user_serializer import UserSerializer
# Create your views here.

class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:    
            UserSerializer({
                'fullname': request.data['fullname'],
                'username': request.data["username"], 
                'email': request.data["email"],
                'password': request.data["password"],
            }).save()
        except KeyError:
            return Response({'message': "Error: The key does not exist in the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'New user has been registered successufully.'}, status=status.HTTP_202_ACCEPTED)

class Login(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Create or get the token
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

