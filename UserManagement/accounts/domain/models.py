from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator


# User Model
class UserProfile(models.Model):
    identity_id = models.IntegerField(null=True, blank=True, unique=True)  # Reference to the Identity service
    full_name = models.CharField(max_length=150, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.full_name


# InstructorRate Model
class InstructorRate(models.Model):
    user_id = models.ForeignKey(
        UserProfile,
        null=False,
        on_delete=models.PROTECT,
        related_name='ratings',
        verbose_name='User who is rating'
    )
    instructor_id = models.ForeignKey(
        UserProfile,
        null=False,
        on_delete=models.PROTECT,
        related_name='instructor_ratings',
        verbose_name='Instructor being rated'
    )

    rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('5.00'))
        ]
    )

    review = models.CharField(null=True, blank=True, max_length=1000)
    rate_date_created = models.DateTimeField(default=timezone.now)  # Timezone-aware datetime
    
    class Meta:
        app_label = 'accounts'

    def __str__(self):
        user_full_name = self.user_id.full_name if self.user_id else "Unknown user"
        instructor_full_name = self.instructor_id.full_name if self.instructor_id else "Unknown user"

        return f"{user_full_name}'s rated {instructor_full_name}: {self.rate}"


