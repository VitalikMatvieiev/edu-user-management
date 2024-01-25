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
    user_id = serializers.IntegerField(source='user.id')
    instructor_id = serializers.IntegerField(source='instructor.id')
    
    class Meta:
        model = InstructorRate
        fields = ['id', 'rate', 'review', 'rate_date_created', 'user_id', 'instructor_id']
        extra_kwargs = {
            'rate_date_created': {'read_only': True},
        }

    def create(self, validated_data):
        # Extract user_id and instructor_id from validated_data
        user_data = validated_data.pop('user', None)
        instructor_data = validated_data.pop('instructor', None)
    
        # Get the UserProfile instances for user and instructor
        user = UserProfile.objects.get(id=user_data['id']) if user_data and 'id' in user_data else None
        instructor = UserProfile.objects.get(id=instructor_data['id']) if instructor_data and 'id' in instructor_data else None
    
        # Create the InstructorRate instance with the UserProfile instances
        instructor_rate = InstructorRate.objects.create(user=user, instructor=instructor, **validated_data)
        return instructor_rate



