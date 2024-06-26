from rest_framework import generics,status,viewsets
from rest_framework.response import Response
from rest_framework.request import Request

from accounts.serializers import SignUpSerializer
from rest_framework.views import APIView
from .tokens import create_jwt_pair_for_user
from django.contrib.auth import authenticate
#=================================Login y Signup========================================


class SignUpView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = SignUpSerializer

    def post(self, request:Request):
        data = request.data

        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
    
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = []

    def post(self,request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email,password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            user_type = user.user_type
            firstname = user.firstname
            response = {"msg": "Login Successfull", "tokens": tokens,"user_type":user_type,"firstname":firstname}
            return Response(data=response, status = status.HTTP_200_OK)
        else:
            return Response(data={"msg": "Invalid email or password"},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request: Request):
        content = {"user":str(request.user),"auth": str(request.auth)}
        return Response(data=content,status = status.HTTP_200_OK)