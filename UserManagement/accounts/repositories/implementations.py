# accounts/repositories/implementations.py

from .interfaces import IUserRepository, IInstructorRateRepository
from ..domain.models import UserProfile, InstructorRate
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class DjangoUserProfileRepository(IUserRepository):
    def get_by_id(self, user_id):
        try:
            return UserProfile.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
        except IntegrityError as e:
            # Handle specific database integrity issues
            # Placeholder for future logging
            # Log the error message: print(f"Integrity error: {e}")
            return None
        except Exception as e:
            # Handle other unexpected exceptions
            # Placeholder for future logging
            # Log the error message: print(f"Unexpected error: {e}")
            return None
        
    def create(self, **kwargs):
        user_profile = UserProfile.objects.create(**kwargs)
        # Handle additional logic specific to user profile creation if necessary
        return user_profile

    def update(self, user_id, **user_data):
        try:
            user = UserProfile.objects.get(id=user_id)
            for field, value in user_data.items():
                setattr(user, field, value)
            user.save()
            return user
        except ObjectDoesNotExist:
            return None
        except IntegrityError as e:
            # Handle specific database integrity issues
            # Placeholder for future logging
            # Log the error message: print(f"Integrity error: {e}")
            return None
        except Exception as e:
            # Handle other unexpected exceptions
            # Placeholder for future logging
            # Log the error message: print(f"Unexpected error: {e}")
            return None

    def delete(self, user_id):
        UserProfile.objects.filter(id=user_id).delete()
        
 
class DjangoInstructorRateRepository(IInstructorRateRepository):
    def get_by_id(self, rate_id):
        try:
            return InstructorRate.objects.get(id=rate_id)
        except ObjectDoesNotExist:
            return None
        except IntegrityError as e:
            # Handle specific database integrity issues
            # Placeholder for future logging
            # Log the error message: print(f"Integrity error: {e}")
            return None
        except Exception as e:
            # Handle other unexpected exceptions
            # Placeholder for future logging
            # Log the error message: print(f"Unexpected error: {e}")
            return None

    def get_all_for_user(self, user_id):
        return InstructorRate.objects.filter(user_id=user_id)

    def create(self, **kwargs):
        rate = InstructorRate.objects.create(**kwargs)
        return rate

    def update(self, rate_id, **rate_data):
        try:
            rate = InstructorRate.objects.get(id=rate_id)
            for field, value in rate_data.items():
                setattr(rate, field, value)
            rate.save()
            return rate
        except ObjectDoesNotExist:
            return None
        except IntegrityError as e:
            # Handle specific database integrity issues
            # Placeholder for future logging
            # Log the error message: print(f"Integrity error: {e}")
            return None
        except Exception as e:
            # Handle other unexpected exceptions
            # Placeholder for future logging
            # Log the error message: print(f"Unexpected error: {e}")
            return None

    def delete(self, rate_id):
        InstructorRate.objects.filter(id=rate_id).delete()
