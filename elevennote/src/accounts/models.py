from django.core.mail import send_mail
from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

import random
import string


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
        """
            Creates and saves a User with the given email and password.
        """
        if email is None:
            raise ValueError('User must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)

        user.code = randomString(10)

        send_mail(
            "Confirm account",
            f"Hello!\nPlease, confirm your email:)\n127.0.0.1:8000/accounts/confirm/{user.code}",
            "yklab.noreply@yandex.ru",
            recipient_list=[email],
            fail_silently=False,
        )

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise ValueError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    code = models.CharField(max_length=10, default="")

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email
