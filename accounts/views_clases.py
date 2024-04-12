from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsOwnerOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import HorarioSerializer, Subjects_with_students_Serializer, SubjectsSerializer,ClaseSerializer

from .models import Clase, Horario, Students,Subjects,Courses, Teachers, User
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class Clases_allView(ModelViewSet):    
    serializer_class = ClaseSerializer       
    queryset = Clase.objects.all()
    def get_queryset(self):
        horario_id = self.request.query_params.get('horario_pk') or None
        if horario_id is not None:
            filtro = Clase.objects.filter(horario_id=horario_id) 
            #queryset = Subjects.objects.all()
            serializer = self.serializer_class(filtro, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_clase(self, clase_id):
        try:
            return Clase.objects.get(id=clase_id)
        except Clase.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_clases(self,request,horario_pk=None,clase_pk=None):
        try:
            filtro = Clase.objects.filter(horario_id=horario_pk) 
            serializer = ClaseSerializer(filtro, many=True)
            return Response(serializer.data)
        except Clase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_clase(self, request,clase_pk=None,horario_pk=None):
        try:
            clase = self.get_clase(clase_id=clase_pk)
            serializer = ClaseSerializer(clase)
            return Response(serializer.data)
        except Clase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_clase(self, request,clase_pk=None,horario_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(horario_id=Horario.objects.get(id=horario_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_clase(self, request,clase_pk=None,horario_pk=None):
        try:
            clase = self.get_clase(clase_id=clase_pk)
            clase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Clase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_clase(self, request,clase_pk=None,horario_pk=None):
        try:
            clase = self.get_clase(clase_id=clase_pk)
            serializer = ClaseSerializer(clase, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Clase.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
