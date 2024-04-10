from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsOwnerOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import Subjects_with_students_Serializer, SubjectsSerializer

from .models import Students,Subjects,Courses, Teachers, User
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class Subjects_allView(ModelViewSet):    
    serializer_class = SubjectsSerializer       
    queryset = Subjects.objects.all()
    def get_queryset(self):
        course_id = self.request.query_params.get('course_pk') or None
        if course_id is not None:
            filtro = Subjects.objects.filter(course_id=course_id) 
            #queryset = Subjects.objects.all()
            serializer = self.serializer_class(filtro, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_subject(self, subject_id):
        try:
            return Subjects.objects.get(id=subject_id)
        except Subjects.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_subjects(self,request,course_pk=None):
        try:
            filtro = Subjects.objects.filter(course_id=course_pk) 
            serializer = SubjectsSerializer(filtro, many=True)
            return Response(serializer.data)
        except Subjects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_subject(self, request, pk=None,course_pk=None):
        try:
            subject = self.get_subject(subject_id=pk)
            serializer = Subjects_with_students_Serializer(subject)
            return Response(serializer.data)
        except Subjects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_subject(self, request, pk=None,course_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(staff_id=self.get_teacher(request),course_id=Courses.objects.get(id=course_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_subject(self, request, pk=None,course_pk=None):
        try:
            subject = self.get_subject(subject_id=pk)
            subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subjects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_subject(self, request, pk=None):
        try:
            subject = self.get_subject(subject_id=pk)
            serializer = Subjects_with_students_Serializer(subject, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Subjects.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
