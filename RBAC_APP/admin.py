from django.contrib import admin
from .models import User, Role, UserRole, Post

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'assigned_at']
    list_filter = ['role', 'assigned_at']
    search_fields = ['user__email', 'role__name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'author']
    search_fields = ['title', 'content', 'author__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
