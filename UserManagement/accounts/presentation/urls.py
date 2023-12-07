from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, InstructorRateViewSet

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'instructorrates', InstructorRateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
