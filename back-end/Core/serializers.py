from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import DoctorProfile, Comment, Reservation

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
            'role',
        )
        read_only_fields = ('id','role')

class DoctorListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')

    class Meta:
        model = DoctorProfile
        fields = [
            'id',
            'name',
            'field',
            'location',
            'score',
            'price',
        ]

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='patient.username')

    class Meta:
        model = Comment
        fields = ['score', 'username', 'comment']

class DoctorDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')
    comments = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = [
            'id',
            'name',
            'field',
            'location',
            'score',
            'price',
            'experience',
            'start_working_hour',
            'end_working_hour',
            'comments',
        ]

    def get_comments(self, obj):
        comments = Comment.objects.filter(doctor=obj.user)
        return CommentSerializer(comments, many=True).data

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            'id',
            'patient',
            'start_reservation_hour',
            'end_reservation_hour'
        ]
        read_only_fields = ['patient']
