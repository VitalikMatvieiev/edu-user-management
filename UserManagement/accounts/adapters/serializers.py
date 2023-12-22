from rest_framework import serializers
from ..domain.models import UserProfile, InstructorRate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'identity_id', 'full_name', 'date_of_birth', ]
        extra_kwargs = {
            'identity_id': {'read_only': True},
        }


class InstructorRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorRate
        fields = '__all__'
        extra_kwargs = {
            'rate_date_created': {'read_only': True},
        }

