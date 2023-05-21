from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'role', 'title', 'blocked_until']


admin.site.register(User, UserAdmin)
