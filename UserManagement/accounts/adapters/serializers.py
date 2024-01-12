from rest_framework import serializers
from ..domain.models import UserProfile, InstructorRate
from ..application.permissions import UpdateUserProfileClaim
from datetime import date


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'identity_id', 'full_name', 'date_of_birth', ]
        extra_kwargs = {
            'identity_id': {'read_only': True},
        }
    
    def validate_full_name(self, value):
        # Ensure the full name is not empty
        if not value.strip():
            raise serializers.ValidationError("Full name cannot be empty.")
        return value
    
    def validate_date_of_birth(self, value):
        # Ensure the date of birth is not in the future
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
    
        # Check if the user is authenticated
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication required to update profile.")
    
        # Raise error if user does not have the 'UpdateUserProfile' claim
        if UpdateUserProfileClaim not in user.claims:
            raise serializers.ValidationError("You do not have permission to update this profile.")
    
        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class InstructorRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorRate
        fields = '__all__'
        extra_kwargs = {
            'rate_date_created': {'read_only': True},
        }
