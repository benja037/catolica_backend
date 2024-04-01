from django.shortcuts import render
from .serializers import SignUpSerializer,SubjectsSerializer,StudentsSerializer,UserSerializer,AttendanceSerializer,AttendanceSerializerOnlyDateandHour
from rest_framework import generics,status,viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from .tokens import create_jwt_pair_for_user

from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView
from django.contrib.auth import authenticate
# Create your views here.
from rest_framework.permissions import IsAuthenticated

from .models import Subjects,Students,User,Attendance





from .permissions import EsCreadorPermiso

class TuModeloDetalle(generics.RetrieveUpdateDestroyAPIView):
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



""" class SubjectsView(viewsets.ModelViewSet):
    serializer_class = ClaseAlumnosSerializer
    queryset = Subjects.objects.all() """


""" class ListaAlumnosClaseAPIView(APIView):
    permission_classes = []
    def get(self, request):
        try:
            clase = Subjects.objects.all()
        except Subjects.DoesNotExist:
            return Response({"error": "La clase no existe"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClaseAlumnosSerializer(clase)
        return Response(serializer.data) """
    
#=================================Simple Views==========================================
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []    

class SubjectsView(ModelViewSet):
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer
    permission_classes = []

class StudentsView(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = []

class AttendanceView(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = []

    

#=================================Login y Signup========================================


class SignUpView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = SignUpSerializer

    def post(self, request:Request):
        data = request.data

        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
    
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = []

    def post(self,request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email,password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status = status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})
        
    def get(self, request: Request):
        content = {"user":str(request.user),"auth": str(request.auth)}
        return Response(data=content,status = status.HTTP_200_OK)
    

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