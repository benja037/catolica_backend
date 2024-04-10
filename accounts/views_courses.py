from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsOwnerOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import CourseSerializer

from .models import Students,Courses, Teachers, User
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsOwnerOrReadOnly & IsProfesorOrReadOnly])
class Courses_allView(ModelViewSet):    
    serializer_class = CourseSerializer       
    queryset = Courses.objects.all()
    def get_queryset(self):        
        filtro = Courses.objects.all()
        #queryset = Courses.objects.all()
        serializer = self.serializer_class(filtro, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except User.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    
    def list_courses(self,request,course_pk=None):
        try:
            filtro = Courses.objects.all()
            serializer = CourseSerializer(filtro, many=True)
            return Response(serializer.data)
        except Courses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_course(self, request,course_pk=None):
        try:
            course = Courses.object.get(id=course_pk)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Courses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_course(self, request,course_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_course(self, request,course_pk=None):
        try:
            course = Courses.objects.get(id=course_pk)
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Courses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_course(self, request,course_pk=None):
        try:
            course = Courses.objects.get(id=course_pk)
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Courses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
