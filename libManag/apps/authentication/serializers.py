from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User

from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    email = serializers.EmailField(validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with this email already exists'
            )
        ])
    password = serializers.CharField(
            max_length=128,
            write_only=True,
            allow_null=True,
            allow_blank=True,
            required=True,
            error_messages={
                'required': 'Password is a required field.',
                'blank': 'Password cannot be blank.'
                }
        )
    username = serializers.RegexField(
        regex='^(?!.*\ )[A-Za-z\d\-\_]+$',
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='A user with this username already exists',
            )
        ],
        error_messages={
            'invalid': 'Username can only contain letters, numbers, underscores, and hyphens',
            'required': 'Username is a required field!'
        })

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                "An email address has to be provided"
            )
        
        if password is None:
            raise serializers.ValidationError(
                "A password is required to log in"
            )
        
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "No user record matches"
            )

        return super().validate(data)
    