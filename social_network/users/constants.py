from django.utils.translation import gettext_lazy as _

# managers.py
# CustomUserManager
CREATE_USER_WITHOUT_EMAIL_ERROR_MESSAGE = _("Email should be provided.")
CREATE_SUPERUSER_WITHOUT_IS_STAFF_ERROR_MESSAGE = (
    "Superuser must have is_staff set to True."
)
CREATE_SUPERUSER_WITHOUT_IS_SUPERUSER_ERROR_MESSAGE = (
    "Superuser must have is_superuser set to True."
)

# serializers.py
# SignUpSerializer
SIGN_UP_SERIALIZER_PASSWORD2_FIELD_LABEL = _("Password confirmation")
SIGN_UP_SERIALIZER_PASSWORD_VALIDATION_ERROR_MESSAGE = _("Password fields didn't match.")
