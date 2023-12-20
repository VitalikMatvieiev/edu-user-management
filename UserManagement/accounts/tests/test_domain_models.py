from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ..domain.models import UserProfile, InstructorRate
from datetime import date, datetime
from decimal import Decimal


class UserProfileTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create(identity_id=123, full_name="John Doe", date_of_birth="1990-01-01")

    def test_user_creation(self):
        user = UserProfile.objects.get(full_name="John Doe")
        self.assertEqual(user.full_name, "John Doe")
        self.assertEqual(user.date_of_birth, date(1990, 1, 1))

    def test_user_str(self):
        user = UserProfile.objects.get(full_name="John Doe")
        self.assertEqual(str(user), "John Doe")

    def test_invalid_date_of_birth(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(full_name="Jane Doe", date_of_birth="invalid-date")
    
    def test_identity_id_unique_constraint(self):
        # This should raise IntegrityError because identity_id must be unique
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(
                identity_id=123,
                full_name="Jane Doe",
                date_of_birth="1995-05-15"
            )

    def test_optional_date_of_birth(self):
        user = UserProfile.objects.create(full_name="Jane Doe")
        self.assertIsNone(user.date_of_birth)


class InstructorRateTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(full_name="Jane Doe", date_of_birth="1992-02-02")
        self.instructor_rate = InstructorRate.objects.create(user=self.user, rate=Decimal('4.5'),
                                                             review="Great instructor")

    def test_rate_creation(self):
        self.assertEqual(self.instructor_rate.rate, Decimal('4.5'))
        self.assertEqual(self.instructor_rate.review, "Great instructor")

    def test_rate_str(self):
        self.assertEqual(str(self.instructor_rate), "Jane Doe's Rating: 4.5")

    def test_default_rate_date_created(self):
        self.assertIsInstance(self.instructor_rate.rate_date_created, datetime)

    def test_rate_decimal_precision(self):
        # This should raise ValidationError due to more than two decimal places
        with self.assertRaises(ValidationError):
            rate = InstructorRate.objects.create(user=self.user, rate=Decimal('4.556'), review="Excellent")
            rate.full_clean()
            rate.save()

    def test_review_length_limit(self):
        long_review = 'a' * 1001  # 1001 characters long
        rate = InstructorRate(user=self.user, rate=Decimal('4.5'), review=long_review)
        with self.assertRaises(ValidationError):
            rate.full_clean()

 

