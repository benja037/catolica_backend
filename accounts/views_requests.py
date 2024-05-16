from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsProfesorOfSubjectOrReadOnly, IsProfesorOrReadOnly
from accounts.serializers import DisciplineSerializer, StudentSubjectRequestSerializer

from .models import Student,Discipline, Subject, Teacher, CustomUser,StudentSubjectRequest
from rest_framework.permissions import IsAuthenticated


""" @permission_classes([IsAuthenticated])
class Requests_Create(ModelViewSet):    
    serializer_class = DisciplineSerializer       
    queryset = Discipline.objects.all()
    def get_queryset(self):        
        all_disciplines = Discipline.objects.all()       
        serializer = self.serializer_class(all_disciplines, many=True)
        return Response(serializer.data)
    
    def list_my_requests(self,request):
        try:
            all_disciplines = Discipline.objects.all()
            serializer = DisciplineSerializer(all_disciplines, many=True)
            return Response(serializer.data)
        except Discipline.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_request(self, request,discipline_pk=None):
        try:
            discipline = Discipline.objects.get(id=discipline_pk)
            serializer = DisciplineSerializer(discipline)
            return Response(serializer.data)
        except Discipline.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_auto_request(self, request):
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
            return Response(status=status.HTTP_404_NOT_FOUND) """
        
    

@permission_classes([IsAuthenticated,IsProfesorOfSubjectOrReadOnly])
class Requests_GetPatch(ModelViewSet):    
    serializer_class = StudentSubjectRequestSerializer       
    queryset = StudentSubjectRequest.objects.all()
    def get_queryset(self):        
        all_request = StudentSubjectRequest.objects.all()       
        serializer = self.serializer_class(all_request, many=True)
        return Response(serializer.data)
    
    def list_requests(self,request,subject_pk):
        try:
            subject = Subject.objects.get(id=subject_pk)
            subjects_request = StudentSubjectRequest.objects.filter(subject=subject)
            serializer = StudentSubjectRequestSerializer(subjects_request, many=True)
            return Response(serializer.data)
        except Discipline.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['patch'])
    def patch_request(self, request,subject_pk=None,request_pk=None):
        try:
            request = StudentSubjectRequest.objects.get(id=request_pk)
            serializer = StudentSubjectRequestSerializer(request, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StudentSubjectRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
