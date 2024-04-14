from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes
from rest_framework.views import APIView

from accounts.permissions import IsOwnerOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import Horario_with_studentes_Serializer, HorarioSerializer, StudentsSerializer, Subjects_with_students_Serializer, SubjectsSerializer

from .models import Horario, Students,Subjects,Courses, Teachers, User
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class Horarios_allView(ModelViewSet):    
    serializer_class = HorarioSerializer       
    queryset = Horario.objects.all()
    def get_queryset(self):
        subject_id = self.request.query_params.get('pk') or None
        if subject_id is not None:
            filtro = Horario.objects.filter(subject_id=subject_id) 
            #queryset = Subjects.objects.all()
            serializer = self.serializer_class(filtro, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_horario(self, horario_id):
        try:
            return Horario.objects.get(id=horario_id)
        except Horario.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_horarios(self,request,pk=None):
        try:
            filtro = Horario.objects.filter(subject_id=pk) 
            serializer = Horario_with_studentes_Serializer(filtro, many=True)
            return Response(serializer.data)
        except Horario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_horario(self, request,horario_pk=None):
        try:
            horario = self.get_horario(horario_id=horario_pk)
            serializer = Horario_with_studentes_Serializer(horario,context={'request':request})#Recordar este cambio a futuro
            return Response(serializer.data)
        except Horario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_horario(self, request, pk=None,horario_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(subject_id=Subjects.objects.get(id=pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_horario(self, request,horario_pk=None):
        try:
            horario = self.get_horario(horario_id=horario_pk)
            horario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Horario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_horario(self, request,horario_pk=None):
        try:
            horario = self.get_horario(horario_id=horario_pk)
            serializer = Horario_with_studentes_Serializer(horario, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Horario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class CursoMateriaAlumnos(ModelViewSet):
    def get_alumnos(self, request, horario_pk):
        try:
            horario = Horario.objects.get(id=horario_pk)
            serializer = StudentsSerializer(horario.alumnos_horario,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Horario.DoesNotExist:
            return Response({"message": "Curso no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

    def post_alumno(self, request, horario_pk=None):
        try:            
            alumno_id = request.data.get('alumno_pk')  # Suponiendo que envías el ID del alumno en el cuerpo de la solicitud
            alumno = Students.objects.get(id=alumno_id)
            horario = Horario.objects.get(id=horario_pk)
            horario.alumnos_horario.add(alumno)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Horario.DoesNotExist:
            return Response({"message": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_alumno(self,request, horario_pk=None):
        try:
            alumno_id = request.data.get('alumno_pk')            
            alumno = Students.objects.get(id=alumno_id)
            horario = Horario.objects.get(id=horario_pk)
            horario.alumnos_horario.remove(alumno)
            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Horario.DoesNotExist:
            return Response({"message": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class HorarioAlumnosAuto(ModelViewSet):
    def get_student(self,request):        
        try:
            student = Students.objects.get(admin=request.user)          #Falta poner que si es profesor no pueda usar esta vista  
            return student
        except Students.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def post_alumno_auto(self, request, horario_pk=None):
        try:            
            alumno = self.get_student(request)  # Suponiendo que envías el ID del alumno en el cuerpo de la solicitud
            #alumno = Students.objects.get(id=alumno_id)
            horario = Horario.objects.get(id=horario_pk)
            horario.alumnos_horario.add(alumno)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Horario.DoesNotExist:
            return Response({"message": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subjects.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_alumno_auto(self,request, horario_pk=None):
        try:
            alumno = self.get_student(request)
            horario = Horario.objects.get(id=horario_pk)
            horario.alumnos_horario.remove(alumno)
            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Horario.DoesNotExist:
            return Response({"message": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        