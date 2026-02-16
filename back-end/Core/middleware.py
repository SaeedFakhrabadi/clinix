import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils import timezone
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class CookieJWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to authenticate users using JWT tokens stored in cookies.
    Handles both access and refresh tokens, automatically refreshing expired
    access tokens when a valid refresh token is present.
    """

    # Paths that don't require authentication
    PUBLIC_PATHS = [
        '/api/v1/auth/',
        '/api/v1/doctors/',
        '/api/v1/doctors/',
        '/api/v1/transactions/create/',
        # Add any other public endpoints
    ]

    def __init__(self, get_response):
        super().__init__(get_response)
        # You can make these configurable via settings
        self.access_token_cookie = getattr(settings, 'JWT_ACCESS_COOKIE_NAME', 'access_token')
        self.refresh_token_cookie = getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh_token')
        self.secure_cookies = getattr(settings, 'JWT_SECURE_COOKIES', not settings.DEBUG)
        self.samesite = getattr(settings, 'JWT_COOKIE_SAMESITE', 'Lax')
        self.access_token_age = getattr(settings, 'JWT_ACCESS_TOKEN_AGE', 5 * 60)  # 5 minutes
        self.refresh_token_age = getattr(settings, 'JWT_REFRESH_TOKEN_AGE', 24 * 60 * 60)  # 24 hours

    def is_public_path(self, path):
        """Check if the path is public and doesn't require authentication."""
        for public_path in self.PUBLIC_PATHS:
            if path.startswith(public_path):
                return True
        return False

    def process_request(self, request):
        """Process incoming request - authenticate user from cookies."""

        # Skip authentication for public paths
        if self.is_public_path(request.path):
            return None

        # Get tokens from cookies
        access_token = request.COOKIES.get(self.access_token_cookie)
        refresh_token = request.COOKIES.get(self.refresh_token_cookie)

        if not access_token and not refresh_token:
            # No tokens - let DRF's permission classes handle unauthorized
            return None

        # Try to authenticate with access token
        user = self.authenticate_with_token(access_token)

        if user:
            # Valid access token - set user on request
            request.user = user
            return None

        # Access token invalid/expired - try to refresh
        if refresh_token:
            new_access_token, user = self.refresh_access_token(refresh_token)
            if new_access_token and user:
                request.user = user
                # Store new access token to be set in response
                request.new_access_token = new_access_token
                return None

        # No valid authentication
        # Let DRF handle unauthorized - don't set user
        return None

    def process_response(self, request, response):
        """Process response - set/update cookies if needed."""

        # Don't modify responses for non-API paths
        if not request.path.startswith('/api/'):
            return response

        # Handle setting new access token from refresh operation
        if hasattr(request, 'new_access_token'):
            self.set_access_token_cookie(response, request.new_access_token)

        # Handle login response (set tokens from response data)
        if hasattr(request, '_auth_tokens'):
            self.set_auth_cookies(response, request._auth_tokens)

        # Handle logout (clear cookies)
        if hasattr(request, '_clear_auth_cookies'):
            self.clear_auth_cookies(response)

        return response

    def authenticate_with_token(self, token):
        """Authenticate user with access token."""
        if not token:
            return None

        try:
            # Validate token
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')

            if not user_id:
                return None

            # Get user from database
            try:
                user = User.objects.get(id=user_id, is_active=True)
                return user
            except User.DoesNotExist:
                return None

        except (TokenError, InvalidToken, jwt.InvalidTokenError) as e:
            logger.debug(f"Token authentication failed: {str(e)}")
            return None

    def refresh_access_token(self, refresh_token):
        """Refresh access token using refresh token."""
        try:
            # Validate refresh token
            refresh = RefreshToken(refresh_token)

            # Check if refresh token is expired
            if self.is_token_expired(refresh):
                return None, None

            # Get user_id from refresh token
            user_id = refresh.payload.get('user_id')
            if not user_id:
                return None, None

            # Get user
            try:
                user = User.objects.get(id=user_id, is_active=True)
            except User.DoesNotExist:
                return None, None

            # Generate new access token
            new_access_token = str(refresh.access_token)

            return new_access_token, user

        except (TokenError, InvalidToken, jwt.InvalidTokenError) as e:
            logger.debug(f"Token refresh failed: {str(e)}")
            return None, None

    def is_token_expired(self, token):
        """Check if token is expired."""
        try:
            exp = token.payload.get('exp')
            if not exp:
                return True
            exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
            return timezone.now() >= exp_datetime
        except Exception:
            return True

    def set_access_token_cookie(self, response, access_token):
        """Set access token cookie on response."""
        response.set_cookie(
            key=self.access_token_cookie,
            value=access_token,
            max_age=self.access_token_age,
            secure=self.secure_cookies,
            httponly=True,
            samesite=self.samesite,
            path='/'
        )

    def set_refresh_token_cookie(self, response, refresh_token):
        """Set refresh token cookie on response."""
        response.set_cookie(
            key=self.refresh_token_cookie,
            value=refresh_token,
            max_age=self.refresh_token_age,
            secure=self.secure_cookies,
            httponly=True,
            samesite=self.samesite,
            path='/'
        )

    def set_auth_cookies(self, response, tokens):
        """Set both access and refresh token cookies."""
        if 'access' in tokens:
            self.set_access_token_cookie(response, tokens['access'])
        if 'refresh' in tokens:
            self.set_refresh_token_cookie(response, tokens['refresh'])

    def clear_auth_cookies(self, response):
        """Clear authentication cookies."""
        response.delete_cookie(self.access_token_cookie, path='/')
        response.delete_cookie(self.refresh_token_cookie, path='/')

