from django.shortcuts import render

from django_crud_api import settings
from .serializers import AddSubjectsSerializer, CourseSerializer, HorarioSerializer, SignUpSerializer,SubjectsSerializer,StudentsSerializer,UserSerializer,AttendanceSerializer,AttendanceSerializerOnlyDateandHour
from rest_framework import generics,status,viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from .tokens import create_jwt_pair_for_user

from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView
from django.contrib.auth import authenticate
# Create your views here.
from rest_framework.permissions import IsAuthenticated

from .models import Horario, Subjects,Students, Teachers,User,Attendance, Courses
from jwt import decode, exceptions




from .permissions import EsCreadorPermiso



#==============================Probando=======================================


class SubjectAttendanceAPIView(APIView):
    permission_classes = []
    def get_subject(self, subject_id):
        try:
            return Subjects.objects.get(id=subject_id)
        except Subjects.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, subject_id, format=None):
        subject = self.get_subject(subject_id)
        students = subject.alumnos.all()
        subject_attendances = Attendance.objects.filter(subject_id=subject_id).distinct('dateandhour')
        serializer = StudentsSerializer(students, many=True)
        
        serializer_attendace = AttendanceSerializerOnlyDateandHour(subject_attendances, many=True)
        return Response(status=status.HTTP_200_OK,data = {"lista_alumnos":serializer.data,"Asistencias":serializer_attendace.data})
    

    def post(self, request, subject_id, format=None):
        subject = self.get_subject(subject_id)
        students = subject.alumnos.all()
        date_get = request.data.get("dateandhour")
        for student in students:
            attendance, created = Attendance.objects.get_or_create(student_id=student, subject_id=subject,dateandhour=date_get)
            estado = request.data.get(str(student.id),False) == 'True'
            attendance.estado = estado
            attendance.save()
        return Response(status=status.HTTP_200_OK,data= {"created":created})
    

        
class SubjectbyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddSubjectsSerializer
    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    

    def get(self,request):
        teacher = self.get_teacher(request)
        #students = subject.alumnos.all()
        subjects_from_user = Subjects.objects.filter(staff_id=teacher.id)
        serializer = SubjectsSerializer(subjects_from_user, many=True)
        
        return Response(status=status.HTTP_200_OK,data = {"subjects_from_teacher":serializer.data})
    
    def post(self,request):
        data = request.data.copy()
        teacher = self.get_teacher(request)
        data["staff_id"] = teacher.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "Subject Created Successfully",
                "data": serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
    
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
""" class TuModeloDetalle(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer
    permission_classes = [EsCreadorPermiso]  # Aplicamos el permiso personalizado

    # Sobreescribimos el método get_object para que se aplique el permiso
    def get_object(self):
        obj = generics.RetrieveUpdateDestroyAPIView.get_object(self)
        self.check_object_permissions(self.request, obj)
        return obj

class EjemploVista(APIView): #Retorna {username:}
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario_actual = request.user
        return Response({"username": usuario_actual.username,"email": usuario_actual.email,"data":usuario_actual})

 """
""" class ProbandoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        token = request.headers['Authorization'].split(' ')[1]
        try:
            payload = decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            user_type = user.user_type
            
            if user_type == 'profesor':
                # Código para la vista del profesor
                return Response({"message": "Vista para profesor"}, status=status.HTTP_200_OK)
            elif user_type == 'alumno':
                # Código para la vista del estudiante
                return Response({"message": "Vista para estudiante"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Tipo de usuario no reconocido"}, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DecodeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND) """