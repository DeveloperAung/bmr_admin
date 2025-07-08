from django.core.management.base import BaseCommand
from api.adminUsers.models import PermissionGroup, Permission, AdminUserRole


class Command(BaseCommand):
    help = 'Create default permission groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write('Creating default permission groups and permissions...')

        # Create Permission Groups
        groups_data = [
            {
                'name': 'user_management',
                'display_name': 'User Management',
                'description': 'Permissions for managing admin users and roles'
            },
            {
                'name': 'content_management',
                'display_name': 'Content Management',
                'description': 'Permissions for managing website content'
            },
            {
                'name': 'event_management',
                'display_name': 'Event Management',
                'description': 'Permissions for managing events'
            },
            {
                'name': 'donation_management',
                'display_name': 'Donation Management',
                'description': 'Permissions for managing donations'
            },
            {
                'name': 'post_management',
                'display_name': 'Post Management',
                'description': 'Permissions for managing posts and articles'
            },
            {
                'name': 'notice_management',
                'display_name': 'Notice Management',
                'description': 'Permissions for managing notices'
            },
            {
                'name': 'membership_management',
                'display_name': 'Membership Management',
                'description': 'Permissions for managing memberships'
            },
            {
                'name': 'system_management',
                'display_name': 'System Management',
                'description': 'Permissions for system-level operations'
            },
        ]

        created_groups = {}
        for group_data in groups_data:
            group, created = PermissionGroup.objects.get_or_create(
                name=group_data['name'],
                defaults=group_data
            )
            created_groups[group_data['name']] = group
            if created:
                self.stdout.write(f'Created permission group: {group.display_name}')
            else:
                self.stdout.write(f'Permission group already exists: {group.display_name}')

        # Create Permissions
        permissions_data = [
            # User Management
            ('user_management', 'user_create', 'Create Users', 'create'),
            ('user_management', 'user_view', 'View Users', 'view'),
            ('user_management', 'user_update', 'Update Users', 'update'),
            ('user_management', 'user_delete', 'Delete Users', 'delete'),
            ('user_management', 'user_soft_delete', 'Soft Delete Users', 'soft_delete'),
            ('user_management', 'role_create', 'Create Roles', 'create'),
            ('user_management', 'role_view', 'View Roles', 'view'),
            ('user_management', 'role_update', 'Update Roles', 'update'),
            ('user_management', 'role_delete', 'Delete Roles', 'delete'),
            ('user_management', 'permission_manage', 'Manage Permissions', 'manage_permissions'),

            # Content Management
            ('content_management', 'content_create', 'Create Content', 'create'),
            ('content_management', 'content_view', 'View Content', 'view'),
            ('content_management', 'content_update', 'Update Content', 'update'),
            ('content_management', 'content_delete', 'Delete Content', 'delete'),
            ('content_management', 'content_publish', 'Publish Content', 'publish'),
            ('content_management', 'content_unpublish', 'Unpublish Content', 'unpublish'),

            # Event Management
            ('event_management', 'event_create', 'Create Events', 'create'),
            ('event_management', 'event_view', 'View Events', 'view'),
            ('event_management', 'event_update', 'Update Events', 'update'),
            ('event_management', 'event_delete', 'Delete Events', 'delete'),
            ('event_management', 'event_publish', 'Publish Events', 'publish'),
            ('event_management', 'event_unpublish', 'Unpublish Events', 'unpublish'),
            ('event_management', 'event_approve', 'Approve Events', 'approve'),
            ('event_management', 'event_reject', 'Reject Events', 'reject'),

            # Donation Management
            ('donation_management', 'donation_create', 'Create Donations', 'create'),
            ('donation_management', 'donation_view', 'View Donations', 'view'),
            ('donation_management', 'donation_update', 'Update Donations', 'update'),
            ('donation_management', 'donation_delete', 'Delete Donations', 'delete'),
            ('donation_management', 'donation_approve', 'Approve Donations', 'approve'),
            ('donation_management', 'donation_reject', 'Reject Donations', 'reject'),
            ('donation_management', 'donation_export', 'Export Donations', 'export'),

            # Post Management
            ('post_management', 'post_create', 'Create Posts', 'create'),
            ('post_management', 'post_view', 'View Posts', 'view'),
            ('post_management', 'post_update', 'Update Posts', 'update'),
            ('post_management', 'post_delete', 'Delete Posts', 'delete'),
            ('post_management', 'post_publish', 'Publish Posts', 'publish'),
            ('post_management', 'post_unpublish', 'Unpublish Posts', 'unpublish'),
            ('post_management', 'post_approve', 'Approve Posts', 'approve'),
            ('post_management', 'post_reject', 'Reject Posts', 'reject'),

            # Notice Management
            ('notice_management', 'notice_create', 'Create Notices', 'create'),
            ('notice_management', 'notice_view', 'View Notices', 'view'),
            ('notice_management', 'notice_update', 'Update Notices', 'update'),
            ('notice_management', 'notice_delete', 'Delete Notices', 'delete'),
            ('notice_management', 'notice_publish', 'Publish Notices', 'publish'),
            ('notice_management', 'notice_unpublish', 'Unpublish Notices', 'unpublish'),

            # Membership Management
            ('membership_management', 'membership_create', 'Create Memberships', 'create'),
            ('membership_management', 'membership_view', 'View Memberships', 'view'),
            ('membership_management', 'membership_update', 'Update Memberships', 'update'),
            ('membership_management', 'membership_delete', 'Delete Memberships', 'delete'),
            ('membership_management', 'membership_approve', 'Approve Memberships', 'approve'),
            ('membership_management', 'membership_reject', 'Reject Memberships', 'reject'),
            ('membership_management', 'membership_export', 'Export Memberships', 'export'),

            # System Management
            ('system_management', 'system_settings_view', 'View System Settings', 'view'),
            ('system_management', 'system_settings_update', 'Update System Settings', 'update'),
            ('system_management', 'audit_logs_view', 'View Audit Logs', 'view_audit_logs'),
            ('system_management', 'backup_create', 'Create Backups', 'create'),
            ('system_management', 'backup_restore', 'Restore Backups', 'custom'),
        ]

        for group_name, perm_name, display_name, perm_type in permissions_data:
            group = created_groups.get(group_name)
            if group:
                permission, created = Permission.objects.get_or_create(
                    name=perm_name,
                    defaults={
                        'display_name': display_name,
                        'permission_type': perm_type,
                        'group': group,
                        'description': f'Permission to {display_name.lower()}'
                    }
                )
                if created:
                    self.stdout.write(f'Created permission: {permission.display_name}')
                else:
                    self.stdout.write(f'Permission already exists: {permission.display_name}')

        # Create default roles
        roles_data = [
            {
                'title': 'Super Admin',
                'description': 'Full system access with all permissions'
            },
            {
                'title': 'Content Manager',
                'description': 'Can manage all content including posts, events, notices'
            },
            {
                'title': 'Event Manager',
                'description': 'Can manage events and related content'
            },
            {
                'title': 'Donation Manager',
                'description': 'Can manage donations and financial records'
            },
            {
                'title': 'User Manager',
                'description': 'Can manage users and basic roles'
            },
            {
                'title': 'Viewer',
                'description': 'Can only view content, no modification permissions'
            },
        ]

        for role_data in roles_data:
            role, created = AdminUserRole.objects.get_or_create(
                title=role_data['title'],
                defaults=role_data
            )
            if created:
                self.stdout.write(f'Created role: {role.title}')
            else:
                self.stdout.write(f'Role already exists: {role.title}')

        # Assign all permissions to Super Admin role
        super_admin_role = AdminUserRole.objects.filter(title='Super Admin').first()
        if super_admin_role:
            all_permissions = Permission.objects.filter(is_active=True)
            super_admin_role.permissions.set(all_permissions)
            self.stdout.write(f'Assigned all permissions to Super Admin role')

        # Assign specific permissions to Content Manager
        content_manager_role = AdminUserRole.objects.filter(title='Content Manager').first()
        if content_manager_role:
            content_permissions = Permission.objects.filter(
                group__name__in=['content_management', 'post_management', 'notice_management'],
                is_active=True
            )
            content_manager_role.permissions.set(content_permissions)
            self.stdout.write(f'Assigned content permissions to Content Manager role')

        # Assign specific permissions to Event Manager
        event_manager_role = AdminUserRole.objects.filter(title='Event Manager').first()
        if event_manager_role:
            event_permissions = Permission.objects.filter(
                group__name='event_management',
                is_active=True
            )
            event_manager_role.permissions.set(event_permissions)
            self.stdout.write(f'Assigned event permissions to Event Manager role')

        # Assign specific permissions to Donation Manager
        donation_manager_role = AdminUserRole.objects.filter(title='Donation Manager').first()
        if donation_manager_role:
            donation_permissions = Permission.objects.filter(
                group__name='donation_management',
                is_active=True
            )
            donation_manager_role.permissions.set(donation_permissions)
            self.stdout.write(f'Assigned donation permissions to Donation Manager role')

        # Assign view permissions to Viewer role
        viewer_role = AdminUserRole.objects.filter(title='Viewer').first()
        if viewer_role:
            view_permissions = Permission.objects.filter(
                permission_type='view',
                is_active=True
            )
            viewer_role.permissions.set(view_permissions)
            self.stdout.write(f'Assigned view permissions to Viewer role')

        self.stdout.write(
            self.style.SUCCESS('Successfully created default permission groups, permissions, and roles!')
        ) 