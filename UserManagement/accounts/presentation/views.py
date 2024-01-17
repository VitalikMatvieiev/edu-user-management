from rest_framework import viewsets, status
from rest_framework.response import Response
from ..domain.models import UserProfile, InstructorRate
from ..adapters.serializers import UserProfileSerializer, InstructorRateSerializer
from ..application.permissions import HasViewUserProfileClaim, HasViewInstructorRateClaim, CanUpdateUserProfile, CanCreateInstructorRate, CreateInstructorRate


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update']:
            permission_classes = [CanUpdateUserProfile]
        else:
            permission_classes = [HasViewUserProfileClaim]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
    
        return Response(serializer.data)
    

class InstructorRateViewSet(viewsets.ModelViewSet):
    queryset = InstructorRate.objects.all()
    serializer_class = InstructorRateSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CanCreateInstructorRate]
        else:
            permission_classes = [HasViewInstructorRateClaim]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    
        # Check if the user has the necessary claim
        if CreateInstructorRate not in request.user.claims:
            return Response({'error': 'You do not have permission'}, status=status.HTTP_403_FORBIDDEN)
        # Ensure that the instructor_id is provided
        instructor_id = request.data.get('instructor_id')
        if not instructor_id:
            return Response({'error': 'Instructor ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Automatically set the user_id to the current user's ID
       #request.data['user_id'] = request.user.identity_id
        
        return super().create(request, *args, **kwargs)

        

