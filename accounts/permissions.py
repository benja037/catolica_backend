from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import status
from accounts.models import Student, Subject, Teacher, CustomUser
from rest_framework.response import Response


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsProfesorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True
        return request.user.user_type=="profesor"
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.user_type=="admin"
    
class IsProfesorOfSubjectOrReadOnly(BasePermission):
    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
          
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True
        else:
            teacher = self.get_teacher(request)
            subject = self.get_subject(view.kwargs['subject_pk'])
            if teacher in subject.teachers.all():
                return True            
        return(False)
    

class IsOwnerofStudent(BasePermission):          
    def has_permission(self, request, view):
        request_user = CustomUser.objects.get(email=request.user)
        student_id = request.query_params.get('student_id')
        student_user = Student.objects.get(id=student_id).user
         
        if request_user != student_user:
            return False            

        if request.user.is_superuser or request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True                   
        return(False)

