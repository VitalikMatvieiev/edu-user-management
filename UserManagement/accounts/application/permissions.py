from rest_framework import permissions

ViewUserProfileClaim = 'ViewUserProfile'
ViewInstructorRateClaim = 'ViewInstructorRate'
UpdateUserProfileClaim = 'UpdateUserProfile'
CreateInstructorRate = 'CreateInstructorRate'
DeleteInstructorRate = 'DeleteInstructorRate'


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


class CanCreateInstructorRate(permissions.BasePermission):
    message = 'Creating instructor rate are not allowed.'
    
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated and CreateInstructorRate in request.user.claims
        return True
    

class CanDeleteInstructorRate(permissions.BasePermission):
    message = 'Delete instructor rate allowed for admin only.'
    
    def has_permission(self, request, view):
        if view.action == 'destroy':
            return request.user.is_authenticated and DeleteInstructorRate in request.user.claims
        return True
    
    
    


    
    