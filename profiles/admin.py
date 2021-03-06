from django.contrib import admin
from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'first_name', 'last_name', 'avatar_img', 'phone', 'date_birth', 'created', 'updated',]
    readonly_fields = ['avatar_img']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    save_on_top = True


