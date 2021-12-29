from random import randint

from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView

from django.contrib.auth.models import User
from .serializer import PollModelSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework import status
from django.contrib.auth.hashers import make_password


from .models import Poll, ForgotPassword



class PollViewSet(CreateAPIView, ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollModelSerializer
    # filter_fields = ['author']
    # search_fields = ['title']

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        print(username, password)
        return Response(serializer.validated_data)
# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class SendCode(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        email = request.GET.get('email')
        try:
            user = User.objects.get(email=email)
        except Exception:
            return Response(data={'answer': "The user with this email was not fount"},
                            status=status.HTTP_204_NO_CONTENT)
        while True:
            code = randint(100000, 1000000)
            temp = ForgotPassword.objects.filter(code=code, is_active=True).count()
            if temp == 0:
                break
        sent_code = ForgotPassword(user=user, code=code)
        sent_code.save()
        return Response(data={'your code': code}, status=status.HTTP_200_OK)

    def post(self, request):
        user = ForgotPassword.objects.get(user__email=request.data.get('email'))
        code = request.data.get('code')
        if user.code == code:
            user.is_active = False
            user.save()
            userone = user.user
            newpass = request.data.get('newpassword')
            userone.password = make_password(newpass)
            userone.save()
            return Response("Your password have been succesfully changed!")
        else:
            return Response("The code is not valid")