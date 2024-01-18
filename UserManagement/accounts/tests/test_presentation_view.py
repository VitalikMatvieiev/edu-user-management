from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from ..domain.models import UserProfile, InstructorRate
from decimal import Decimal


class MockUserProfile(UserProfile):
    is_authenticated = True
    claims = []
    identity_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_authenticated = True


class UserProfileViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_profile = UserProfile.objects.create(full_name="Jane Doe", date_of_birth="1995-05-15")
        self.detail_url = reverse('userprofile-detail', kwargs={'pk': self.user_profile.id})
        
        # Create a mock user with claims
        self.mock_user = MockUserProfile(full_name="Test User", identity_id=self.user_profile.id)
    
    def test_updateUserProfile_Success_WithProperPermissions(self):
        """
        UpdateUserProfile should succeed when the user has proper permissions.
        """
        self.mock_user.claims = ['UpdateUserProfile']
        self.client.force_authenticate(user=self.mock_user)
        
        response = self.client.put(self.detail_url, {'full_name': 'Updated Name'})
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.full_name, 'Updated Name')
    
    def test_updateUserProfile_Forbidden_WithoutProperClaims(self):
        """
        UpdateUserProfile should be forbidden when the user lacks proper claims.
        """
        self.mock_user.claims = []
        self.client.force_authenticate(user=self.mock_user)
        
        response = self.client.put(self.detail_url, {'full_name': 'Updated Name'})
        self.assertEqual(response.status_code, 403)
    
    def test_updateUserProfile_Forbidden_ForAnonymousUser(self):
        """
        UpdateUserProfile should be forbidden for an anonymous user.
        """
        self.client.force_authenticate(user=AnonymousUser())
        
        response = self.client.put(self.detail_url, {'full_name': 'Updated Name'})
        self.assertEqual(response.status_code, 403)


class InstructorRateViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create and save a user and an instructor for testing
        self.user = UserProfile.objects.create(full_name="Test User")
        self.instructor = UserProfile.objects.create(full_name="Test Instructor")
        
        # Create mock user and instructor with claims
        self.mock_user = MockUserProfile(full_name="Mock User", identity_id=self.user.id)
        self.mock_instructor = MockUserProfile(full_name="Mock Instructor", identity_id=self.instructor.id)
        
        # Initialize with default claims
        self.mock_user.claims = ['ViewInstructorRate']
        self.mock_instructor.claims = []
        
        # Authenticate the mock user
        self.client.force_authenticate(user=self.mock_user)
        
        # Create the instructor rate with the saved user and instructor
        self.instructor_rate = InstructorRate.objects.create(
            user_id=self.user,
            instructor_id=self.instructor,
            rate=Decimal('4.5'),
            review="Excellent"
        )
        self.list_url = reverse('instructorrate-list')
    
    def test_getInstructorRates_OnValidRequest_ReturnsListOfInstructorRates(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_createInstructorRate_Success_WithProperPermissions(self):
        self.mock_user.claims = ['CreateInstructorRate']
        self.client.force_authenticate(user=self.mock_user)
    
        data = {
            'instructor_id': self.instructor.id,
            'user_id': self.user.id,
            'rate': 4.5,
            'review': 'Excellent'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 201, response.data)
    
    def test_createInstructorRate_Forbidden_WithoutProperClaims(self):
        self.mock_user.claims = []
        self.client.force_authenticate(user=self.mock_user)
        
        data = {'instructor_id': self.instructor.id, 'rate': 4.5, 'review': 'Excellent'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 403)
    
    def test_deleteInstructorRate_Success_AsAdmin(self):
        self.mock_user.claims = ['DeleteInstructorRateAdminOnly']
        self.client.force_authenticate(user=self.mock_user)
        
        response = self.client.delete(reverse('instructorrate-detail', args=[self.instructor_rate.id]))
        self.assertEqual(response.status_code, 204)
    
    def test_deleteInstructorRate_Forbidden_ForNonAdminUser(self):
        self.mock_user.claims = []
        self.client.force_authenticate(user=self.mock_user)
        
        response = self.client.delete(reverse('instructorrate-detail', args=[self.instructor_rate.id]))
        self.assertEqual(response.status_code, 403)

