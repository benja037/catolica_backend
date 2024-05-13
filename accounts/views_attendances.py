from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsProfesorOrReadOnly,IsProfesorOfSubjectOrReadOnly
from accounts.serializers import AttendanceSerializer, AttendanceSerializerNameLastname, AttendanceSerializerOnlyStateChange

from .models import Attendance, ClassInstance, StudentGroup, Student,Subject,Discipline, Teacher, CustomUser
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsProfesorOfSubjectOrReadOnly])
class Attendances_allView(ModelViewSet):    
    serializer_class = AttendanceSerializer       
    queryset = Attendance.objects.all()
    def get_queryset(self):
        class_pk = self.request.query_params.get('class_pk') or None
        if class_pk is not None:
            class_instances = Attendance.objects.filter(class_instance=class_pk)             
            serializer = self.serializer_class(class_instances, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_attendance(self, attendance_id):
        try:
            return Attendance.objects.get(id=attendance_id)
        except Attendance.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_attendances(self,request,class_pk=None,attendance_pk=None):
        try:            
            attendances = Attendance.objects.filter(class_instance=class_pk) 
            serializer = AttendanceSerializerNameLastname(attendances, many=True)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_attendance(self, request,attendance_pk=None):
        try:
            attendance = Attendance.objects.get(id=attendance_pk)             
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_attendance(self, request,class_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(class_instance=ClassInstance.objects.get(id=class_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_attendance(self, request,attendance_pk=None):
        try:
            attendance = self.get_attendance(attendance_id=attendance_pk)
            attendance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_attendance(self, request,attendance_pk=None):
        try:
            attendance = self.get_attendance(attendance_id=attendance_pk)
            serializer = AttendanceSerializerOnlyStateChange(attendance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsProfesorOfSubjectOrReadOnly])
class AttendanceOfClass(ModelViewSet):        

    def create_default(self, request, class_pk=None,):
        try:
            class_instance = ClassInstance.objects.get(id=class_pk)              
            students = class_instance.alumnos
            for student in students:
                student_id = student.get('id')
                Attendance.objects.create(class_instance=class_instance,student = Student.objects.get(id=student_id),state=False,user_previous_state="no-responde")
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except ClassInstance.DoesNotExist:
            return Response({"message": "Clase no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
    