from django.db import models
from django.utils import timezone


# User Model
class UserProfile(models.Model):
    identity_id = models.IntegerField(null=True, blank=True, unique=True)  # Reference to the Identity service
    full_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

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


