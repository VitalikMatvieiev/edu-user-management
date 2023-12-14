from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone


# User Model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    identity_id = models.IntegerField(null=True, blank=True)  # Reference to the Identity service
    full_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'date_of_birth']  # Customize as needed

    def __str__(self):
        return self.full_name


# InstructorRate Model
class InstructorRate(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.PROTECT, related_name='ratings')
    rate = models.FloatField()
    review = models.TextField(null=True, blank=True)
    rate_date_created = models.DateTimeField(default=timezone.now)  # Timezone-aware datetime

    def __str__(self):
        user_full_name = self.user.full_name if self.user else "Unknown user"
        return f"{user_full_name}'s Rating: {self.rate}"


