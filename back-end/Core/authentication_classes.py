from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
import jwt

User = get_user_model()


class CookieJWTAuthentication(BaseAuthentication):
    """
    Custom authentication class that reads JWT from cookies
    """

    def authenticate(self, request):
        # Get token from cookie
        access_token = request.COOKIES.get(settings.JWT_ACCESS_COOKIE_NAME)

        if not access_token:
            return None  # No authentication attempt made

        try:
            # Validate token
            access_token_obj = AccessToken(access_token)
            user_id = access_token_obj.payload.get('user_id')

            if not user_id:
                return None

            # Get user from database
            try:
                user = User.objects.get(id=user_id, is_active=True)
                return (user, None)
            except User.DoesNotExist:
                return None

        except (TokenError, InvalidToken, jwt.InvalidTokenError) as e:
            # Token invalid - let the middleware handle refresh if needed
            return None

    def authenticate_header(self, request):
        return 'Cookie'