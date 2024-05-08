from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsProfesorOrReadOnly
from accounts.serializers import DisciplineSerializer

from .models import Student,Discipline, Teacher, CustomUser
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsProfesorOrReadOnly])
class Disciplines_allView(ModelViewSet):    
    serializer_class = DisciplineSerializer       
    queryset = Discipline.objects.all()
    def get_queryset(self):        
        all_disciplines = Discipline.objects.all()
        #queryset = Courses.objects.all()
        serializer = self.serializer_class(all_disciplines, many=True)
        return Response(serializer.data)
    
    def list_disciplines(self,request,course_pk=None):
        try:
            all_disciplines = Discipline.objects.all()
            serializer = DisciplineSerializer(all_disciplines, many=True)
            return Response(serializer.data)
        except Discipline.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_Discipline(self, request,discipline_pk=None):
        try:
            discipline = Discipline.object.get(id=discipline_pk)
            serializer = DisciplineSerializer(discipline)
            return Response(serializer.data)
        except Discipline.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_discipline(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_discipline(self, request,discipline_pk=None):
        try:
            discipline = Discipline.objects.get(id=discipline_pk)
            discipline.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Discipline.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_discipline(self, request,discipline_pk=None):
        try:
            discipline = Discipline.objects.get(id=discipline_pk)
            serializer = DisciplineSerializer(discipline, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Discipline.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
