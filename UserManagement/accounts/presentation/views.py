from rest_framework import viewsets
from rest_framework.response import Response
from ..domain.models import UserProfile, InstructorRate
from ..adapters.serializers import UserProfileSerializer, InstructorRateSerializer
from ..application.permissions import HasViewUserProfileClaim, HasViewInstructorRateClaim, CanUpdateUserProfile
from django.views.decorators.csrf import csrf_exempt


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
    permission_classes = [HasViewInstructorRateClaim]
    queryset = InstructorRate.objects.all()
    serializer_class = InstructorRateSerializer

