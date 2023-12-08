from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.db import IntegrityError


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, identity_id=None, **extra_fields):
        """
        Creates and saves a User with the given email, identity_id, and password.
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
        Creates and saves an admin user with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
    
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Admin user must have is_admin=True.')
    
        return self.create_user(email, identity_id, **extra_fields)

    def create_instructor_user(self, email, identity_id=None, **extra_fields):
        """
        Creates and saves an instructor user with the given email and password.
        """
        extra_fields.setdefault('is_instructor', True)
    
        if extra_fields.get('is_instructor') is not True:
            raise ValueError('Instructor user must have is_instructor=True.')
    
        return self.create_user(email, identity_id, **extra_fields)


# User Model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    identity_id = models.IntegerField(null=True, blank=True)  # Reference to the Identity service
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'date_of_birth']  # Customize as needed

    def __str__(self):
        return self.email


# InstructorRate Model
class InstructorRate(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='ratings')
    rate = models.FloatField()
    review = models.TextField(null=True, blank=True)
    rate_date_created = models.DateTimeField(default=timezone.now)  # Timezone-aware datetime

    def __str__(self):
        user_full_name = self.user.full_name if self.user else "Unknown user"
        return f"{user_full_name}'s Rating: {self.rate}"


