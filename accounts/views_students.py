from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsProfesorOrReadOnly
from accounts.serializers import SimpleStudentSerializer, StudentSerializer

from .models import Student
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsProfesorOrReadOnly])
class Students_allView(ModelViewSet):    
    serializer_class = StudentSerializer       
    queryset = Student.objects.all()
    def get_queryset(self):        
        all_students = Student.objects.all()       
        serializer = self.serializer_class(all_students, many=True)
        return Response(serializer.data)
    
    def list_students(self,request):
        try:
            all_students = Student.objects.all()
            serializer = SimpleStudentSerializer(all_students, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_student(self, request,student_pk=None):
        try:
            student = Student.objects.get(id=student_pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_student(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_student(self, request,student_pk=None):
        try:
            student = Student.objects.get(id=student_pk)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_student(self, request,student_pk=None):
        try:
            student = Student.objects.get(id=student_pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#Get students of user "apoderado"      
@permission_classes([IsAuthenticated])
class Students_of_userView(ModelViewSet):    
    serializer_class = StudentSerializer       
    queryset = Student.objects.all()
    def get_queryset(self):        
        all_students = Student.objects.all()       
        serializer = self.serializer_class(all_students, many=True)
        return Response(serializer.data)
    
    def list_students_of_user(self,request):
        try:
            students_of_user = Student.objects.filter(user=request.user)
            serializer = SimpleStudentSerializer(students_of_user, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'])
    def create_student_of_user(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)