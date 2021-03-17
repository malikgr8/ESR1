from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import re
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


@api_view(['POST'])
def signup(request):
    regex = r"(03[0-9]{2}[0-9]{7})$"
    mobile_number = request.data.get('mobile_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not re.search(regex, mobile_number):
        raise ValidationError('moblile number is invalid')
    password = request.data.get('password')
    if len(password) < 8:
        raise ValidationError('password length should be greater than 8')
    if not first_name or not last_name:
        raise ValidationError('Both First Name and Last Name are required')
    try:
        user = User(
            username=mobile_number,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        return Response('user successfully registerd')
    except:
        return Response('user registration failed.')


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def login(request, format=None):
    content = {
        'message': 'login successful'
    }
    return Response(content)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response('Logged out successfully.')


class ChangePassowrdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data.get('new_password')
        if len(new_password) < 8:
            raise ValidationError('password length should be greater than 8')
        user = request.user
        user.password = make_password(new_password)
        user.save()
        logout(request)
        return Response('Password changed successfully. Please login again with new password')

  
@api_view(['POST'])
def authenticate(request):
    data = {
        'status': 0
    }
    user = None

    try:
        uid = request.POST['uid']
        phone = request.POST['phone']

        if User.objects.filter(username=phone).exists():
            user = auth.authenticate(
                username=phone, password=uid
            )
        else:
            user = User.objects.create_user(
                username=phone, password=uid
            )

        if user:
            data['status'] = 1
    except Exception as e:
        print(e)
        pass

    return Response(data=data)
