from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'

    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    google_id = models.CharField(max_length=30)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
