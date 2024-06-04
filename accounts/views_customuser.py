from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes
from accounts.serializers import SimpleStudentSerializer, StudentSerializer, UserSerializer

from .models import CustomUser
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsAuthenticated])
class CustomUser_allView(ModelViewSet):    
    serializer_class = UserSerializer      
    def retrieve_customuser(self,request):
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            
            serializer = UserSerializer(customuser)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
