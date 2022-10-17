from django.contrib.auth.base_user import BaseUserManager
from users import constants


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where the unique identifier
    for authentication is email instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(constants.CREATE_USER_WITHOUT_EMAIL_ERROR_MESSAGE)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(constants.CREATE_SUPERUSER_WITHOUT_IS_STAFF_ERROR_MESSAGE)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                constants.CREATE_SUPERUSER_WITHOUT_IS_SUPERUSER_ERROR_MESSAGE
            )
        return self.create_user(email, password, **extra_fields)
