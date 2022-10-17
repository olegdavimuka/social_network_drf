from django.contrib.auth import get_user_model, login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import constants


class SignUpSerializer(serializers.ModelSerializer):
    """
    Define the Sign Up API representation.
    """

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
            )
        ],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label=constants.SIGN_UP_SERIALIZER_PASSWORD2_FIELD_LABEL,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "email",
            "password",
            "password2",
        )

    def validate(self, attrs):
        """
        Check that the two password entries match
        """

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password": constants.SIGN_UP_SERIALIZER_PASSWORD_VALIDATION_ERROR_MESSAGE  # noqa: E501
                }
            )
        return attrs

    def create(self, validated_data):
        """
        Create a new user with encrypted password, login and return it.
        """

        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=True,
        )

        login(self.context["request"], user)
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    A user serializer to return the username, email, and groups.
    """

    password = serializers.CharField(write_only=True, required=False)
    last_login = serializers.DateTimeField(read_only=True)
    last_activity = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "url",
            "username",
            "email",
            "last_login",
            "last_activity",
            "password",
        )

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """

        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """

        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
