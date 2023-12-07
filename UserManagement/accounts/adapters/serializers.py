from rest_framework import serializers
from ..domain.models import UserProfile, InstructorRate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # List all fields or specify a list of fields


class InstructorRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorRate
        fields = '__all__'

