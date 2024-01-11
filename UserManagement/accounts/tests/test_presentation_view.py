from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..domain.models import UserProfile, InstructorRate


class MockUserProfile(UserProfile):
    is_authenticated = True
    claims = []
    identity_id = None


class UserProfileViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_profile = UserProfile.objects.create(full_name="Jane Doe", date_of_birth="1995-05-15")
        self.detail_url = reverse('userprofile-detail', kwargs={'pk': self.user_profile.id})
        
        # Create a mock user with claims
        self.mock_user = MockUserProfile(full_name="Test User", identity_id=self.user_profile.id)
        self.mock_user.claims = ['UpdateUserProfile']
    
    def test_updateUserProfile_Success_WithProperPermissions(self):
        """
        UpdateUserProfile should succeed when the user has proper permissions.
        """
        self.client.force_authenticate(user=self.mock_user)
        
        response = self.client.put(self.detail_url, {'full_name': 'Updated Name'})
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.full_name, 'Updated Name')
    
    def test_updateUserProfile_Forbidden_WithoutProperClaims(self):
        """
        UpdateUserProfile should be forbidden when the user lacks proper claims.
        """
        # Test with a user without proper claims
        self.mock_user.claims = []
        self.client.force_authenticate(user=self.mock_user)
        
        response = self.client.put(self.detail_url, {'full_name': 'Updated Name'})
        self.assertEqual(response.status_code, 403)
    
    def test_updateUserProfile_Forbidden_ForAnonymousUser(self):
        """
        UpdateUserProfile should be forbidden for an anonymous user.
        """
        # Test with an anonymous user
        self.client.force_authenticate(user=AnonymousUser())
        
        response = self.client.put(self.detail_url, {'full_name': 'Updated Name'})
        self.assertEqual(response.status_code, 403)


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

    def test_getInstructorRates_OnValidRequest_ReturnsListOfInstructorRates(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    # Additional tests for create, retrieve, update, destroy

