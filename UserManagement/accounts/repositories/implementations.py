# accounts/repositories/implementations.py

from .interfaces import IUserRepository, IInstructorRateRepository
from ..domain.models import UserProfile, InstructorRate
from django.core.exceptions import ObjectDoesNotExist


class DjangoUserProfileRepository(IUserRepository):
    def get_by_id(self, user_id):
        try:
            return UserProfile.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None

    def create(self, **kwargs):
        user_profile = UserProfile.objects.create(**kwargs)
        # Handle additional logic specific to user profile creation if necessary
        return user_profile

    def update(self, user_id, **kwargs):
        UserProfile.objects.filter(id=user_id).update(**kwargs)
        return self.get_by_id(user_id)

    def delete(self, user_id):
        UserProfile.objects.filter(id=user_id).delete()


class DjangoInstructorRateRepository(IInstructorRateRepository):
    def get_by_id(self, rate_id):
        try:
            return InstructorRate.objects.get(id=rate_id)
        except ObjectDoesNotExist:
            return None

    def get_all_for_user(self, user_id):
        return InstructorRate.objects.filter(user_id=user_id)

    def create(self, **kwargs):
        rate = InstructorRate.objects.create(**kwargs)
        return rate

    def update(self, rate_id, **kwargs):
        InstructorRate.objects.filter(id=rate_id).update(**kwargs)
        return self.get_by_id(rate_id)

    def delete(self, rate_id):
        InstructorRate.objects.filter(id=rate_id).delete()
