from rest_framework import viewsets
from ..domain.models import UserProfile, InstructorRate
from ..adapters.serializers import UserProfileSerializer, InstructorRateSerializer
from ..application.permissions import HasViewUserProfileClaim, HasViewInstructorRateClaim


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [HasViewUserProfileClaim]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    

class InstructorRateViewSet(viewsets.ModelViewSet):
    permission_classes = [HasViewInstructorRateClaim]
    queryset = InstructorRate.objects.all()
    serializer_class = InstructorRateSerializer

