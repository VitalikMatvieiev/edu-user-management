from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..domain.models import UserProfile, InstructorRate


class MockUserProfile(UserProfile):
    # Add a claims attribute for testing purposes
    claims = []


class UserProfileViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a mock user with claims
        self.mock_user = MockUserProfile(full_name="Test User")
        self.mock_user.claims = ['ViewUserProfile']
        # Authenticate the mock user
        self.client.force_authenticate(user=self.mock_user)
        self.list_url = reverse('userprofile-list')

    def test_list_user_profiles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)


class InstructorRateViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create and save a user for testing
        self.user = UserProfile.objects.create(full_name="Test User")
        # Manually add the claims attribute to the user instance
        self.user.claims = ['ViewInstructorRate']
        
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        
        # Create the instructor rate with the saved user
        self.instructor_rate = InstructorRate.objects.create(user=self.user, rate=4.5, review="Excellent")
        self.list_url = reverse('instructorrate-list')

    def test_list_instructor_rates(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # Additional tests for create, retrieve, update, destroy

