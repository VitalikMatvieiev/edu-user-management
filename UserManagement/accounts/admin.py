from django.contrib import admin
from .domain.models import UserProfile, InstructorRate

admin.site.register(UserProfile)
admin.site.register(InstructorRate)
