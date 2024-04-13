from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsOwnerOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import StudentsSerializer, Subjects_with_students_Serializer, SubjectsSerializer

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
            serializer = Subjects_with_students_Serializer(subject,context={'request':request})
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

#@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
@permission_classes([IsAuthenticated])
class SubjectsAlumnos(ModelViewSet):
    def get_alumnos(self, request, pk=None):
        try:
            subject = Subjects.objects.get(id=pk)
            serializer = StudentsSerializer(subject.alumnos,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subjects.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

    def post_alumno(self, request, pk=None):
        try:            
            alumno_id = request.data.get('alumno_pk')  # Suponiendo que envías el ID del alumno en el cuerpo de la solicitud
            alumno = Students.objects.get(id=alumno_id)
            subject = Subjects.objects.get(id=pk)
            subject.alumnos.add(alumno)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subjects.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_alumno(self,request, pk=None):
        try:
            alumno_id = request.data.get('alumno_pk')            
            alumno = Students.objects.get(id=alumno_id)
            subject = Subjects.objects.get(id=pk)
            subject.alumnos.remove(alumno)
            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subjects.DoesNotExist:
            return Response({"message": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsAuthenticated])
class SubjectsAlumnosAuto(ModelViewSet):
    def get_student(self,request):        
        try:
            student = Students.objects.get(admin=request.user)          #Falta poner que si es profesor no pueda usar esta vista  
            return student
        except Students.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def post_alumno_auto(self, request, pk=None):
        try:            
            alumno = self.get_student(request)  # Suponiendo que envías el ID del alumno en el cuerpo de la solicitud
            #alumno = Students.objects.get(id=alumno_id)
            subject = Subjects.objects.get(id=pk)
            subject.alumnos.add(alumno)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subjects.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_alumno_auto(self,request, pk=None):
        try:
            alumno = self.get_student(request)
            subject = Subjects.objects.get(id=pk)
            subject.alumnos.remove(alumno)
            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Students.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subjects.DoesNotExist:
            return Response({"message": "Horario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        