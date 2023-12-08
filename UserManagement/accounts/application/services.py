from ..repositories.interfaces import IUserRepository, IInstructorRateRepository
from ..repositories.implementations import DjangoUserProfileRepository, DjangoInstructorRateRepository

# TODO: Need to add exceptions


class UserProfileService:
    def __init__(self, user_repository: IUserRepository = None):
        self.user_repository = user_repository or DjangoUserProfileRepository()

    def register_user_profile(self, **user_data):
        # Validate user_data, perform any additional logic and create a user profile
        user_profile = self.user_repository.create(**user_data)
        return user_profile

    def update_user_profile(self, user_id, **user_data):
        # Perform any necessary validation and business logic checks
        updated_user_profile = self.user_repository.update(user_id, **user_data)
        return updated_user_profile

    def delete_user_profile(self, user_id):
        # You can place additional checks here if needed before deletion
        self.user_repository.delete(user_id)

    def get_user_profile(self, user_id):
        # Additional logic can be placed here if you want to manipulate the data in any way
        user_profile = self.user_repository.get_by_id(user_id)
        return user_profile


class InstructorRateService:
    def __init__(self, instructor_rate_repository: IInstructorRateRepository = None):
        self.instructor_rate_repository = instructor_rate_repository or DjangoInstructorRateRepository()

    def add_instructor_rating(self, **rate_data):
        # Validate rate_data, perform any additional logic and create an instructor rate
        instructor_rate = self.instructor_rate_repository.create(**rate_data)
        return instructor_rate

    def update_instructor_rating(self, rate_id, **rate_data):
        # Perform any necessary validation and business logic checks
        updated_instructor_rate = self.instructor_rate_repository.update(rate_id, **rate_data)
        return updated_instructor_rate

    def delete_instructor_rating(self, rate_id):
        # You can place additional checks here if needed before deletion
        self.instructor_rate_repository.delete(rate_id)

    def get_instructor_rating(self, rate_id):
        # Additional logic can be placed here if you want to manipulate the data in any way
        instructor_rate = self.instructor_rate_repository.get_by_id(rate_id)
        return instructor_rate

    def get_all_ratings_for_instructor(self, user_id):
        # Fetch all ratings for a specific instructor
        all_ratings = self.instructor_rate_repository.get_all_for_user(user_id)
        return all_ratings

