from django.core.management.base import BaseCommand
from RBAC_APP.models import Role


class Command(BaseCommand):
    help = 'Initialize blog RBAC with Reader, Editor, and Author roles'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing Blog RBAC System...'))

        # Create Roles
        roles = [
            {'name': Role.READER, 'description': 'Can read/view published posts'},
            {'name': Role.EDITOR, 'description': 'Can create and edit draft posts'},
            {'name': Role.AUTHOR, 'description': 'Can publish, delete posts and manage users'},
        ]

        for role_data in roles:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={'description': role_data['description']}
            )
            status = 'Created' if created else 'Already exists'
            self.stdout.write(
                self.style.SUCCESS(f"✓ Role '{role.get_name_display()}': {status}")
            )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Blog RBAC initialization completed successfully!')
        )
