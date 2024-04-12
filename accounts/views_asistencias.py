from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsOwnerOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import AttendanceSerializer, AttendanceSerializerOnlyEstadoChange, Horario_with_studentes_Serializer, HorarioSerializer, StudentsSerializer, Subjects_with_students_Serializer, SubjectsSerializer,ClaseSerializer

from .models import Attendance, Clase, Horario, Students,Subjects,Courses, Teachers, User
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class Asistencias_allView(ModelViewSet):    
    serializer_class = AttendanceSerializer       
    queryset = Attendance.objects.all()
    def get_queryset(self):
        clase_id = self.request.query_params.get('clase_pk') or None
        if clase_id is not None:
            filtro = Attendance.objects.filter(clase_id=clase_id) 
            #queryset = Subjects.objects.all()
            serializer = self.serializer_class(filtro, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_asistencia(self, asistencia_id):
        try:
            return Attendance.objects.get(id=asistencia_id)
        except Attendance.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_asistencias(self,request,clase_pk=None,asistencia_pk=None):
        try:            
            filtro = Attendance.objects.filter(clase_id=clase_pk) 
            serializer = AttendanceSerializer(filtro, many=True)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_asistencia(self, request,asistencia_pk=None,clase_pk=None):
        try:
            filtro = Attendance.objects.filter(clase_id=clase_pk) 
            asistencia = filtro.get(id=asistencia_pk)
            serializer = AttendanceSerializer(asistencia)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_asistencia(self, request,clase_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(clase_id=Clase.objects.get(id=clase_pk)) #Poner la clase_id luego el student_id por body
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_asistencia(self, request,asistencia_pk=None,clase_pk=None):
        try:
            asistencia = self.get_asistencia(asistencia_id=asistencia_pk)
            asistencia.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_asistencia(self, request,asistencia_pk=None,clase_pk=None):
        try:
            asistencia = self.get_asistencia(asistencia_id=asistencia_pk)
            serializer = AttendanceSerializerOnlyEstadoChange(asistencia, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class AttendanceOfClass(ModelViewSet):        

    def create_default(self, request, clase_pk=None,):
        try:
            clase = Clase.objects.get(id=clase_pk)            
            horario_id = clase.horario_id
            horario = Horario.objects.get(id=horario_id.id)
            #alumnos= horario.alumnos_horario
            serializer = Horario_with_studentes_Serializer(horario)
            alumnos = serializer.data.get('alumnos_horario',[])
            for student in alumnos:
                student_id = student.get('id')
                Attendance.objects.create(clase_id=clase,student_id = Students.objects.get(id=student_id),estado=False,user_estado_previo="no-responde")
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Clase.DoesNotExist:
            return Response({"message": "Clase no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Horario.DoesNotExist:
            return Response({"message": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)        
    