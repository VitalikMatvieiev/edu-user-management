from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ..domain.models import UserProfile, InstructorRate
from django.utils import timezone
from datetime import date, datetime
from django.db import transaction


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
        self.instructor_rate = InstructorRate.objects.create(user=self.user, rate=4.5, review="Great instructor")

    def test_rate_creation(self):
        self.assertEqual(self.instructor_rate.rate, 4.5)
        self.assertEqual(self.instructor_rate.review, "Great instructor")

    def test_rate_str(self):
        self.assertEqual(str(self.instructor_rate), "Jane Doe's Rating: 4.5")

    def test_default_rate_date_created(self):
        self.assertIsInstance(self.instructor_rate.rate_date_created, datetime)

 

