from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Get content type for Book model
        book_content_type = ContentType.objects.get_for_model(Book)

        # Get custom permissions defined in Book model
        can_view = Permission.objects.get(codename='can_view', content_type=book_content_type)
        can_create = Permission.objects.get(codename='can_create', content_type=book_content_type)
        can_edit = Permission.objects.get(codename='can_edit', content_type=book_content_type)
        can_delete = Permission.objects.get(codename='can_delete', content_type=book_content_type)

        # Create groups
        viewers, created = Group.objects.get_or_create(name='Viewers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created group: Viewers'))
        else:
            self.stdout.write(self.style.WARNING('Group already exists: Viewers'))
        
        editors, created = Group.objects.get_or_create(name='Editors')
        if created:
            self.stdout.write(self.style.SUCCESS('Created group: Editors'))
        else:
            self.stdout.write(self.style.WARNING('Group already exists: Editors'))
        
        admins, created = Group.objects.get_or_create(name='Admins')
        if created:
            self.stdout.write(self.style.SUCCESS('Created group: Admins'))
        else:
            self.stdout.write(self.style.WARNING('Group already exists: Admins'))

        # Assign permissions to Viewers (read-only)
        viewers.permissions.set([can_view])
        self.stdout.write(self.style.SUCCESS('Assigned permissions to Viewers: can_view'))

        # Assign permissions to Editors (can view, add, change)
        editors.permissions.set([can_view, can_create, can_edit])
        self.stdout.write(self.style.SUCCESS('Assigned permissions to Editors: can_view, can_create, can_edit'))

        # Assign permissions to Admins (all permissions)
        admins.permissions.set([can_view, can_create, can_edit, can_delete])
        self.stdout.write(self.style.SUCCESS('Assigned permissions to Admins: all book permissions'))

        self.stdout.write(self.style.SUCCESS('✅ Successfully set up groups and permissions!'))
