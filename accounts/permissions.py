from rest_framework.permissions import BasePermission, SAFE_METHODS


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