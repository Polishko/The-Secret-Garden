from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

import logging

logger = logging.getLogger(__name__)

class AppUserManager(BaseUserManager):
    """
    Internal helper method to create and save a regular user with the given username, email, and password.
    This method enforces default roles for all users.
    """
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)

        """
        Forcing default role for all users created outside the admin panel
        """
        extra_fields.setdefault('role', 'customer')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        logger.info(f"Creating user with username: {username}, email: {email}")

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user, role customer with the given username, email, and password.
        """
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser, role admin with the given username, email, and password.
        """
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
