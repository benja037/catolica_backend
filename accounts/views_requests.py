from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsProfesorOfSubjectOrReadOnly, IsProfesorOrReadOnly
from accounts.serializers import DisciplineSerializer, StudentSubjectRequestSerializer

from .models import Student,Discipline, Subject, Teacher, CustomUser,StudentSubjectRequest
from rest_framework.permissions import IsAuthenticated



        
    

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
            subjects_request = StudentSubjectRequest.objects.filter(subject=subject,state='pendiente')
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
        
    @action(detail=True, methods=['patch'])
    def acceptordeny_subject_request(self, request,subject_pk=None,request_pk=None):        
        subject = get_object_or_404(Subject,id=subject_pk)
        studentsubjectrequest = get_object_or_404(StudentSubjectRequest,id=request_pk)
        accept = request.data.get('accept')
        if accept is not None:
            if accept == True:
                subject.students.add(studentsubjectrequest.student)
                studentsubjectrequest.state = 'aceptado'
            elif accept == False:
                studentsubjectrequest.state = 'rechazado'
            studentsubjectrequest.save()
            return Response({'status': 'Solicitud actualizada'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'El campo "accept" es requerido'}, status=status.HTTP_400_BAD_REQUEST)

