from django.contrib import admin
from user_management.UserManagement.accounts.domain.models import UserProfile, InstructorRate

admin.site.register(UserProfile)
admin.site.register(InstructorRate)
