from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ..domain.models import UserProfile, InstructorRate
from datetime import date, datetime
from decimal import Decimal


class UserProfileTestCase(TestCase):
    def setUp(self):
        UserProfile.objects.create(identity_id=123, full_name="John Doe", date_of_birth="1990-01-01")

    def test_create_userProfile_createsValidUser_onValidData(self):
        user = UserProfile.objects.get(full_name="John Doe")
        self.assertEqual(user.full_name, "John Doe")
        self.assertEqual(user.date_of_birth, date(1990, 1, 1))

    def test_str_returnsFullName_onUserProfileInstance(self):
        user = UserProfile.objects.get(full_name="John Doe")
        self.assertEqual(str(user), "John Doe")

    def test_create_userProfile_raisesValidationError_onInvalidDateOfBirth(self):
        with self.assertRaises(ValidationError):
            UserProfile.objects.create(full_name="Jane Doe", date_of_birth="invalid-date")
    
    def test_create_userProfile_raisesIntegrityError_onDuplicateIdentityId(self):
        # This should raise IntegrityError because identity_id must be unique
        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(
                identity_id=123,
                full_name="Jane Doe",
                date_of_birth="1995-05-15"
            )

    def test_create_userProfile_createsUserWithoutDateOfBirth_onMissingDateOfBirth(self):
        user = UserProfile.objects.create(full_name="Jane Doe")
        self.assertIsNone(user.date_of_birth)


class InstructorRateTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(full_name="Jane Doe", date_of_birth="1992-02-02")
        self.instructor_rate = InstructorRate.objects.create(user=self.user, rate=Decimal('4.5'), review="Great instructor")

    def test_instructorRateCreation_WithValidData_CreatesSuccessfully(self):
        self.assertEqual(self.instructor_rate.rate, Decimal('4.5'))
        self.assertEqual(self.instructor_rate.review, "Great instructor")

    def test_instructorRateStr_ReturnsFormattedString(self):
        expected_string = "Jane Doe's Rating: 4.5"
        self.assertEqual(str(self.instructor_rate), expected_string)

    def test_instructorRateCreation_SetsCurrentDateTime_OnRateDateCreated(self):
        self.assertIsInstance(self.instructor_rate.rate_date_created, datetime)

    def test_instructorRateCreation_WithInvalidDecimalPrecision_RaisesValidationError(self):
        with self.assertRaises(ValidationError):
            rate = InstructorRate(user=self.user, rate=Decimal('4.556'), review="Excellent")
            rate.full_clean()

    def test_instructorRateCreation_WithReviewExceedingLengthLimit_RaisesValidationError(self):
        long_review = 'a' * 1001  # 1001 characters long
        rate = InstructorRate(user=self.user, rate=Decimal('4.5'), review=long_review)
        with self.assertRaises(ValidationError):
            rate.full_clean()

    def test_instructorRateCreation_WithRateBelowMinimum_RaisesValidationError(self):
        with self.assertRaises(ValidationError):
            rate = InstructorRate(user=self.user, rate=Decimal('-1.0'), review="Poor")
            rate.full_clean()

    def test_instructorRateCreation_WithRateAboveMaximum_RaisesValidationError(self):
        with self.assertRaises(ValidationError):
            rate = InstructorRate(user=self.user, rate=Decimal('5.1'), review="Excellent")
            rate.full_clean()


 

