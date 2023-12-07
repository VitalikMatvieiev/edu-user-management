from rest_framework import viewsets
from ..domain.models import UserProfile, InstructorRate
from ..adapters.serializers import UserProfileSerializer, InstructorRateSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class InstructorRateViewSet(viewsets.ModelViewSet):
    queryset = InstructorRate.objects.all()
    serializer_class = InstructorRateSerializer

