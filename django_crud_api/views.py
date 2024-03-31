""" from rest_framework.decorators  import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
#from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password']) 
        user.save()

        
        return Response({"user": serializer.data},status = status.HTTP_201_CREATED)

    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    print(request.user)



    return Response("You are login with {}".format(request.user.username),status = status.HTTP_200_OK) """