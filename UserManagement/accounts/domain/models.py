from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, identity_id=None, **extra_fields):
        """
        Creates and saves a User with the given email, identity_id, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not identity_id:
            raise ValueError('Users must have an associated identity_id')

        user = self.model(
            email=self.normalize_email(email),
            identity_id=identity_id,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, identity_id=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, identity_id, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            email=email,
            password=password,
            identity_id=identity_id,
            **extra_fields
        )
 

# User Model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    identityId = models.IntegerField(null=True, blank=True)  # Reference to the Identity service
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'date_of_birth']  # Customize as needed

    def __str__(self):
        return self.email


# InstructorRate Model
class InstructorRate(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='ratings')
    rate = models.FloatField()
    review = models.TextField(null=True, blank=True)
    rate_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        user_full_name = self.user.full_name if self.user else "Unknown user"
        return f"{user_full_name}'s Rating: {self.rate}"


