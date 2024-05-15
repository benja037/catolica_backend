from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes
from rest_framework.views import APIView

from accounts.permissions import IsProfesorOrReadOnly
from accounts.serializers import StudentGroupPostSerializer, StudentGroupSerializer, StudentSerializer

from .models import  Student,Subject,Discipline, Teacher, CustomUser,StudentGroup
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsProfesorOrReadOnly])
class StudentGroups_allView(ModelViewSet):    
    serializer_class = StudentGroupSerializer       
    queryset = StudentGroup.objects.all()
    def get_queryset(self):
        subject_pk = self.request.query_params.get('subject_pk') or None
        if subject_pk is not None:
            groups = StudentGroup.objects.filter(subject=subject_pk)             
            serializer = self.serializer_class(groups, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_grupo(self, group_id):
        try:
            return StudentGroup.objects.get(id=group_id)
        except StudentGroup.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_groups(self,request,subject_pk=None):
        try:
            groups = StudentGroup.objects.filter(subject=subject_pk) 
            serializer = StudentGroupSerializer(groups, many=True)
            return Response(serializer.data)
        except StudentGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_group(self, request,group_pk=None):
        try:
            group = self.get_grupo(group_id=group_pk)
            serializer = StudentGroupSerializer(group,context={'request':request})
            return Response(serializer.data)
        except StudentGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_group(self, request, subject_pk=None):
        serializer = StudentGroupPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(subject=Subject.objects.get(id=subject_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_group(self, request,group_pk=None):
        try:
            group = self.get_group(group_id=group_pk)
            group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StudentGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_group(self, request,group_pk=None):
        try:
            group = self.get_group(group_id=group_pk)
            serializer = StudentGroupSerializer(group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StudentGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsProfesorOrReadOnly])
class ManageStudentOfGroup(ModelViewSet):
    def get_students_of_group(self, request, group_pk=None):
        try:
            group = StudentGroup.objects.get(id=group_pk)
            serializer = StudentGroupSerializer(group.students,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentGroup.DoesNotExist:
            return Response({"message": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

    def post_student_to_group(self, request, group_pk=None):
        try:            
            student_id = request.data.get('student_pk')  
            student = Student.objects.get(id=student_id)
            group = StudentGroup.objects.get(id=group_pk)
            group.students.add(student)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except StudentGroup.DoesNotExist:
            return Response({"message": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_student_of_group(self,request, group_pk=None):
        try:
            student_id = request.data.get('student_pk')            
            student = Student.objects.get(id=student_id)
            group = StudentGroup.objects.get(id=group_pk)
            group.students.remove(student)
            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except StudentGroup.DoesNotExist:
            return Response({"message": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
