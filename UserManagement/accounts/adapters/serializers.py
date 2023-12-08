from rest_framework import serializers
from ..domain.models import UserProfile, InstructorRate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # List all fields or specify a list of fields
        extra_kwargs = {
            'email': {'read_only': True},  # Make 'email' read-only after creation
        }


class InstructorRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorRate
        fields = '__all__'
        extra_kwargs = {
            'rate_date_created': {'read_only': True},  # Make 'email' read-only after creation
        }

