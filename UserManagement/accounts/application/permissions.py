from rest_framework import permissions


class HasViewUserProfileClaim(permissions.BasePermission):
    message = 'Viewing user profiles is not allowed.'
    
    def has_permission(self, request, view):
        return 'ViewUserProfile' in request.user.claims


class HasViewInstructorRateClaim(permissions.BasePermission):
    message = 'Viewing instructor rates is not allowed.'
    
    def has_permission(self, request, view):
        return 'ViewInstructorRate' in request.user.claims
    
    