from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):     
    password = serializers.CharField(
        write_only=True,
        # validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phonenumber')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phonenumber=validated_data['phonenumber'],
            password=validated_data['password'],
            role="PATIENT"
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
    identifier = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    verificationCode = serializers.IntegerField(required=True)
    newPassword = serializers.CharField(
        required=True,
        write_only=True,
        # validators=[validate_password],
        style={'input_type': 'password'}
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phonenumber',
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

