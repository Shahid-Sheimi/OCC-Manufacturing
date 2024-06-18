# permissions.py

from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners of an object or admin users to access it.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, AnonymousUser):
            # The user is not authenticated
            return False 
        return obj.user == request.user or request.user.is_staff
    

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners of an object or admin users to access it.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, AnonymousUser):
            # The user is not authenticated
            return False 
        
        return  request.user.is_superuser
