from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    AdminUser, 
    AdminUserRole, 
    Permission, 
    PermissionGroup, 
    UserAuditLog, 
    AdminUserRoleAuditLog, 
    PermissionAuditLog
)


@admin.register(PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'display_name', 'description']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    ordering = ['name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'display_name', 'description', 'is_active')
        }),
        ('System Information', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'permission_type', 'group', 'is_active']
    list_filter = ['permission_type', 'group', 'is_active', 'created_at']
    search_fields = ['name', 'display_name', 'description', 'group__name']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    ordering = ['group__name', 'display_name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'display_name', 'permission_type', 'group', 'description', 'is_active')
        }),
        ('System Information', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class RolePermissionInline(admin.TabularInline):
    model = AdminUserRole.permissions.through
    extra = 1
    verbose_name = "Permission"
    verbose_name_plural = "Permissions"


@admin.register(AdminUserRole)
class AdminUserRoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'permission_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    ordering = ['title']
    inlines = [RolePermissionInline]
    exclude = ('permissions',)  # Exclude the M2M field from the main form

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('System Information', {
            'fields': ('uuid', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def permission_count(self, obj):
        return obj.permissions.count()
    permission_count.short_description = 'Permissions Count'


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'email', 'admin_user_role', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'admin_user_role', 'date_joined']
    search_fields = ['username', 'name', 'email', 'contact']
    readonly_fields = ['uuid', 'date_joined', 'last_login']
    ordering = ['username']

    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'name', 'email', 'password')
        }),
        ('Contact Information', {
            'fields': ('contact', 'secondary_contact')
        }),
        ('Role & Permissions', {
            'fields': ('admin_user_role',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('uuid',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('admin_user_role')


@admin.register(UserAuditLog)
class UserAuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'performed_by', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'user__name', 'performed_by__username']
    readonly_fields = ['user', 'action', 'performed_by', 'timestamp']
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AdminUserRoleAuditLog)
class AdminUserRoleAuditLogAdmin(admin.ModelAdmin):
    list_display = ['admin_user_role', 'action', 'performed_by', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['admin_user_role__title', 'performed_by__username']
    readonly_fields = ['admin_user_role', 'action', 'performed_by', 'timestamp']
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PermissionAuditLog)
class PermissionAuditLogAdmin(admin.ModelAdmin):
    list_display = ['permission', 'action', 'performed_by', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['permission__name', 'permission__display_name', 'performed_by__username']
    readonly_fields = ['permission', 'action', 'performed_by', 'timestamp', 'details']
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
