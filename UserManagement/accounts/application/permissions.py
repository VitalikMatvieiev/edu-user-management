from rest_framework import permissions

ViewUserProfileClaim = 'ViewUserProfile'
ViewInstructorRateClaim = 'ViewInstructorRate'
UpdateUserProfileClaim = 'UpdateUserProfile'


class HasViewUserProfileClaim(permissions.BasePermission):
    message = 'Viewing user profiles is not allowed.'
    
    def has_permission(self, request, view):
        return ViewUserProfileClaim in request.user.claims
        

class HasViewInstructorRateClaim(permissions.BasePermission):
    message = 'Viewing instructor rates is not allowed.'
    
    def has_permission(self, request, view):
        return ViewInstructorRateClaim in request.user.claims


class CanUpdateUserProfile(permissions.BasePermission):
    message = 'Update user profile is not allowed.'
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        return UpdateUserProfileClaim in request.user.claims

    
    