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
from django.core.exceptions import ObjectDoesNotExist


PASSWORD_REGEX = r"(?=.*?[0-9])"

@api_view(['POST'])
def signup(request):
    regex = r"(03[0-9]{2}[0-9]{7})$"
    mobile_number = request.data.get('mobile_number')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not re.search(regex, mobile_number):
        raise ValidationError('moblile number is invalid')
    mobile_number = '{}{}'.format('+92', mobile_number[1:])

    password = request.data.get('password')
    if len(password) < 8:
        raise ValidationError('password length should be greater or eqaul than 8')
    if not re.search(PASSWORD_REGEX, password):
        raise ValidationError('password must have atleast one digit in it')
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
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if len(new_password) < 8:
            raise ValidationError('password length should be greater than 8')
        if not re.search(PASSWORD_REGEX, new_password):
            raise ValidationError('password must have atleast one digit in it')
        user = request.user
        if user.check_password(new_password):
            raise ValidationError('You can not set old password as new password')
        user.password = make_password(new_password)
        user.save()
        logout(request)
        return Response('Password changed successfully. Please login again with new password')


class ForgotPassowrdView(APIView):

    def post(self, request):
        password_regex = r"(?=.*?[0-9])"
        mobile_number = request.data.get('mobile_number')
        if not mobile_number:
            raise ValidationError('mobile_number missing')
        mobile_number = '{}{}'.format('+92', mobile_number[1:])
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
    
        if new_password != confirm_password:
            raise ValidationError('New password does not match confirm password.')
        if len(new_password) < 8:
            raise ValidationError('password length should be greater or equal than 8')
        if not re.search(PASSWORD_REGEX, new_password):
            raise ValidationError('password must have atleast one digit in it')
        try:
            user = User.objects.get(username=mobile_number)
        except ObjectDoesNotExist:
            raise ValidationError('Invalid mobile number')
        
        user.password = make_password(new_password)
        user.save()
        logout(request)
        return Response('Password changed successfully. Please login with new password')


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        email = request.data.get('email', '')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        try:
            user.save()
            return Response('User info updated succesfully.')
        except:
            return Response('something went wrong please try again.')


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
