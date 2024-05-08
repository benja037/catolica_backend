from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsProfesorOrReadOnly
from accounts.serializers import ClassInstanceSerializer

from .models import Discipline, StudentGroup, Student,Subject,ClassInstance, Teacher, CustomUser
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsProfesorOrReadOnly])
class ClassInstance_allView(ModelViewSet):    
    serializer_class = ClassInstanceSerializer       
    queryset = ClassInstance.objects.all()
    def get_queryset(self):
        subject_pk = self.request.query_params.get('subject_pk') or None
        if subject_pk is not None:
            classInstances = ClassInstance.objects.filter(subject=subject_pk)             
            serializer = self.serializer_class(classInstances, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_class(self, class_id):
        try:
            return ClassInstance.objects.get(id=class_id)
        except ClassInstance.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_class(self,request,subject_pk=None):
        try:
            classInstances = ClassInstance.objects.filter(subject=subject_pk) 
            serializer = ClassInstanceSerializer(classInstances, many=True)
            return Response(serializer.data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_class(self, request,class_pk=None):
        try:
            classInstance = self.get_class(class_id=class_pk)
            serializer = ClassInstanceSerializer(classInstance)
            return Response(serializer.data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_class(self, request,subject_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(subject=Subject.objects.get(id=subject_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_class(self, request,class_pk=None):
        try:
            classInstance = self.get_class(class_id=class_pk)
            classInstance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_class(self, request,class_pk=None):
        try:
            classInstance = self.get_class(class_id=class_pk)
            serializer = ClassInstanceSerializer(classInstance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #Hay que arreglar los errores las excepciones
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsProfesorOrReadOnly])
class Subjects_Class_allView(ModelViewSet):
    serializer_class = ClassInstanceSerializer
    queryset = ClassInstance.objects.all()
    
    def list(self,request,subject_pk=None,date=None):
        try:       
            classInstances = ClassInstance.objects.filter(subject=subject_pk, date=date)            
            class_data = ClassInstanceSerializer(classInstances, many=True).data                
            return Response(class_data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        