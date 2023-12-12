from django.contrib.auth.models import BaseUserManager
from django.db import IntegrityError

# Custom User Manager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, identity_id=None, **extra_fields):
        """
        Creates and saves a User with the given email and identity_id.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        if identity_id is None:
            raise ValueError('Users must have an identity_id')
        
        try:
            user = self.model(
                email=self.normalize_email(email),
                identity_id=identity_id,
                **extra_fields
            )
            user.save(using=self._db)
            return user
        except IntegrityError:
            raise ValueError('A user with that email already exists.')
    
    def create_admin_user(self, email, identity_id=None, **extra_fields):
        """
        Creates and saves an admin user with the given email.
        """
        extra_fields.setdefault('is_admin', True)
        
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Admin user must have is_admin=True.')
        
        return self.create_user(email, identity_id, **extra_fields)
    
    def create_instructor_user(self, email, identity_id=None, **extra_fields):
        """
        Creates and saves an instructor user with the given email.
        """
        extra_fields.setdefault('is_instructor', True)
        
        if extra_fields.get('is_instructor') is not True:
            raise ValueError('Instructor user must have is_instructor=True.')
        
        return self.create_user(email, identity_id, **extra_fields)
