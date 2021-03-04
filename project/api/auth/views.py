from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User


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
