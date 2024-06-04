from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import IsProfesorOrReadOnly,IsProfesorOfSubjectOrReadOnly
from accounts.serializers import AttendanceHistorySerializer, AttendanceSerializer, AttendanceSerializerNameLastname, AttendanceSerializerOnlyStateChange

from .models import Attendance, ClassInstance, StudentGroup, Student,Subject,Discipline, Teacher, CustomUser,AttendanceHistory
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
    
    def list_attendances(self,request,class_pk=None,attendance_pk=None,subject_pk=None):
        try:            
            attendances = Attendance.objects.filter(class_instance=class_pk) 
            serializer = AttendanceSerializerNameLastname(attendances, many=True)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_attendance(self, request,attendance_pk=None,subject_pk=None):
        try:
            attendance = Attendance.objects.get(id=attendance_pk)             
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_attendance(self, request,class_pk=None,subject_pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(class_instance=ClassInstance.objects.get(id=class_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_attendance(self, request,attendance_pk=None,subject_pk=None):
        try:
            attendance = self.get_attendance(attendance_id=attendance_pk)
            attendance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['put'])
    def update_attendance(self, request,attendance_pk=None,subject_pk=None):
        try:
            attendance = self.get_attendance(attendance_id=attendance_pk)
            serializer = AttendanceSerializerOnlyStateChange(attendance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Attendance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsAuthenticated])
class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type=='profesor':
            return Attendance.objects.filter(class_instance__professor=user)
        else:
            return Attendance.objects.filter(student=user.id)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def student_update_attendance(self, request, attendance_pk=None):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            print(request.user.id)
            print(attendance_pk)
            print(request.user.id)
            instance = Attendance.objects.get(id=attendance_pk)
        except Attendance.DoesNotExist:
            return Response({'detail': 'Not found or not permitted.'}, status=status.HTTP_404_NOT_FOUND)

        if user.user_type=='profesor':
            return Response({'detail': 'Professors cannot update this field.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'user_previous_state' in serializer.validated_data:
            AttendanceHistory.objects.create(
                attendance=instance,
                user_previous_state=serializer.validated_data['user_previous_state'],
                changed_by=request.user
            )
        self.perform_update(serializer)
        return Response(serializer.data)