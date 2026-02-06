from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        if identifier is None or password is None:
            return None

        try:
            # Try to find user by email or phonenumber
            user = User.objects.get(
                models.Q(email__iexact=identifier) |
                models.Q(phonenumber=identifier)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

        # Check password
        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
