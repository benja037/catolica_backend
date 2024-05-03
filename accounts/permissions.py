from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import status
from accounts.models import Subjects, Teachers, User
from rest_framework.response import Response

class EsCreadorPermiso(BasePermission):
    """
    Permiso que solo permite al creador del objeto realizar actualizaciones.
    """
    def has_object_permission(self, request, view, obj):
        # Verifica si el usuario es el creador del objeto
        return obj.staff_id == request.user  # Asumiendo que hay un campo "user" en el modelo que indica el creador del objeto
    



class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Allow admin users to perform any action.
        if request.user.is_staff:
            return True

        # Check if the user is the owner of the object.
        return obj.created_by == request.user
    
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    
class IsProfesorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.user_type=="profesor"
    
class IsProfesorOfSubjectOrReadOnly(BasePermission):
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
          
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            teacher = self.get_teacher(request)
            subject = self.get_subject(view.kwargs['pk'])
            if teacher in subject.profesores.all():
                return True            
        return(False)