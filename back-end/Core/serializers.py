from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import UserRoles

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):     
    password = serializers.CharField(write_only=True, validators=[validate_password])

    role = serializers.ChoiceField(
        choices=UserRoles.choices,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phonenumber', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phonenumber=validated_data['phonenumber'],
            password=validated_data['password'],
            role=validated_data['role'],
        )

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if not identifier or not password:
            raise serializers.ValidationError("Both identifier and password are required.")

        return attrs

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    reset_id = serializers.UUIDField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        label="Confirm password"
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match.",
                "password2": "Password fields didn't match."
            })
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phonenumber',
            'role',
        )
        read_only_fields = ('id', 'role')

class DoctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'specialty',
            'clinic_name',
            'price_per_visit',
        )

class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    message_en = serializers.CharField()
    code = serializers.CharField(required=False, allow_blank=True)

