from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email

from user.models import User

from getpass import getpass


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            email = input('Email: ')
            if not email:
                continue
            else:
                try:
                    validate_email(email)
                except ValidationError:
                    self.stderr.write('Invalid email address.')
                    continue

            admin = input('Shall be admin (y/N): ')
            if admin.lower() not in ('y', 'n'):
                continue

            is_admin = admin.lower() == 'y'

            pw = getpass()
            if not pw:
                continue

            pw2 = getpass('Repeat Password: ')
            if not pw2:
                continue
            elif pw != pw2:
                self.stderr.write('Passwords do not match.')
                continue

            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                user = User.objects.create_user(email, pw, is_admin=is_admin, is_active=True)
                self.stdout.write('User created with id %d.' % user.id)
                break
            else:
                self.stderr.write('User already exists with email address %r (id %d).' % (user.email, user.id))
                continue
