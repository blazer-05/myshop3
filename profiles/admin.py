from django.contrib import admin
from profiles.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'first_name', 'last_name', 'avatar', 'phone', 'date_birth', 'created', 'updated',]

