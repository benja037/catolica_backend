from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes
from rest_framework.views import APIView

from accounts.permissions import IsOwnerOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import GrupoAlumnosSerializer, StudentsSerializer, Subjects_with_students_Serializer, SubjectsSerializer

from .models import  Students,Subjects,Courses, Teachers, User,GrupoAlumnos
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class Grupos_allView(ModelViewSet):    
    serializer_class = GrupoAlumnosSerializer       
    queryset = GrupoAlumnos.objects.all()
    def get_queryset(self):
        subject_id = self.request.query_params.get('pk') or None
        if subject_id is not None:
            filtro = GrupoAlumnos.objects.filter(subject_id=subject_id) 
            #queryset = Subjects.objects.all()
            serializer = self.serializer_class(filtro, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_grupo(self, grupo_id):
        try:
            return GrupoAlumnos.objects.get(id=grupo_id)
        except GrupoAlumnos.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_grupos(self,request,pk=None):
        try:
            filtro = GrupoAlumnos.objects.filter(subject_id=pk) 
            serializer = GrupoAlumnosSerializer(filtro, many=True)
            return Response(serializer.data)
        except GrupoAlumnos.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_grupo(self, request,grupo_pk=None):
        try:
            grupo = self.get_grupo(grupo_id=grupo_pk)
            serializer = GrupoAlumnosSerializer(grupo,context={'request':request})#Recordar este cambio a futuro
            return Response(serializer.data)
        except GrupoAlumnos.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_grupo(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(subject_id=Subjects.objects.get(id=pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_grupo(self, request,grupo_pk=None):
        try:
            grupo = self.get_grupo(grupo_id=grupo_pk)
            grupo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GrupoAlumnos.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_grupo(self, request,grupo_pk=None):
        try:
            grupo = self.get_grupo(grupo_id=grupo_pk)
            serializer = GrupoAlumnosSerializer(grupo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except GrupoAlumnos.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class CursoMateriaAlumnos(ModelViewSet):
    def get_alumnos(self, request, grupo_pk):
        try:
            grupo = GrupoAlumnos.objects.get(id=grupo_pk)
            serializer = StudentsSerializer(grupo.alumnos,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GrupoAlumnos.DoesNotExist:
            return Response({"message": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

    def post_alumno(self, request, grupo_pk=None):
        try:            
            alumno_id = request.data.get('alumno_pk')  # Suponiendo que envías el ID del alumno en el cuerpo de la solicitud
            alumno = Students.objects.get(id=alumno_id)
            grupo = GrupoAlumnos.objects.get(id=grupo_pk)
            grupo.alumnos.add(alumno)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except GrupoAlumnos.DoesNotExist:
            return Response({"message": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_alumno(self,request, grupo_pk=None):
        try:
            alumno_id = request.data.get('alumno_pk')            
            alumno = Students.objects.get(id=alumno_id)
            grupo = GrupoAlumnos.objects.get(id=grupo_pk)
            grupo.alumnos.remove(alumno)
            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except GrupoAlumnos.DoesNotExist:
            return Response({"message": "Grupo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

""" @permission_classes([IsAuthenticated])
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
        
         """