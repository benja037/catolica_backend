from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsOwnerOrReadOnly,ReadOnly
from accounts.serializers import Subjects_with_students_Serializer, SubjectsSerializer

from .models import Students,Subjects,Courses, Teachers, User
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/ 

@permission_classes([IsOwnerOrReadOnly])
class Subjects_allView(ModelViewSet):    
    serializer_class = SubjectsSerializer       
    #queryset = Subjects.objects.all()
    def get_queryset(self):
        queryset = Subjects.objects.all()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def get_subject(self, subject_id):
        try:
            return Subjects.objects.get(id=subject_id)
        except Subjects.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list(self, request):
        queryset = Subjects.objects.all()
        serializer = SubjectsSerializer(queryset, many=True)
        return Response(serializer.data)