from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class IsAdminOrMember(permissions.BasePermission):
    """
    Custom permission to only allow admins or members to access.
    """
    def has_permission(self, request, view):
        # Check if the user is an admin or a member

        if isinstance(request.user, AnonymousUser):
            # The user is not authenticated
            return False 
        return request.user.is_superuser or request.user.role=='member' or request.user.role=='admin'
    

class NoPostPermission(permissions.BasePermission):
    """
    Custom permission to deny POST requests.
    """

    def has_permission(self, request, view):
        # Allow GET, PUT, PATCH, DELETE requests
        return request.method in ['GET', 'PUT', 'PATCH', 'DELETE']