from rest_framework.permissions import BasePermission


class EsCreadorPermiso(BasePermission):
    """
    Permiso que solo permite al creador del objeto realizar actualizaciones.
    """
    def has_object_permission(self, request, view, obj):
        # Verifica si el usuario es el creador del objeto
        return obj.staff_id == request.user  # Asumiendo que hay un campo "user" en el modelo que indica el creador del objeto