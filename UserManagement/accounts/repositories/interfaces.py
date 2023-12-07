from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id):
        """Retrieve a User instance by its ID."""
        pass

    @abstractmethod
    def create(self, **kwargs):
        """Create a new User instance."""
        pass

    @abstractmethod
    def update(self, user_id, **kwargs):
        """Update an existing User instance."""
        pass

    @abstractmethod
    def delete(self, user_id):
        """Delete a User instance."""
        pass


class IInstructorRateRepository(ABC):
    @abstractmethod
    def get_by_id(self, rate_id):
        """Retrieve an InstructorRate instance by its ID."""
        pass

    @abstractmethod
    def get_all_for_user(self, user_id):
        """Retrieve all InstructorRate instances for a User."""
        pass

    @abstractmethod
    def create(self, **kwargs):
        """Create a new InstructorRate instance."""
        pass

    @abstractmethod
    def update(self, rate_id, **kwargs):
        """Update an existing InstructorRate instance."""
        pass

    @abstractmethod
    def delete(self, rate_id):
        """Delete an InstructorRate instance."""
        pass

