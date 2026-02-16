# auth_utils.py
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class CookieAuthMixin:
    """
    Mixin to handle cookie-based authentication in views.
    """

    def set_auth_cookies(self, response, user):
        """
        Generate JWT tokens and set them as cookies on the response.
        Returns the response object for chaining.
        """
        refresh = RefreshToken.for_user(user)

        # Set access token cookie
        response.set_cookie(
            key=settings.JWT_ACCESS_COOKIE_NAME,
            value=str(refresh.access_token),
            max_age=settings.JWT_ACCESS_TOKEN_AGE,
            secure=settings.JWT_SECURE_COOKIES,
            httponly=True,
            samesite=settings.JWT_COOKIE_SAMESITE,
            path='/'
        )

        # Set refresh token cookie
        response.set_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            value=str(refresh),
            max_age=settings.JWT_REFRESH_TOKEN_AGE,
            secure=settings.JWT_SECURE_COOKIES,
            httponly=True,
            samesite=settings.JWT_COOKIE_SAMESITE,
            path='/'
        )

        return response  # Important: return the response

    def clear_auth_cookies(self, response):
        """
        Clear authentication cookies.
        Returns the response object for chaining.
        """
        response.delete_cookie(settings.JWT_ACCESS_COOKIE_NAME, path='/')
        response.delete_cookie(settings.JWT_REFRESH_COOKIE_NAME, path='/')
        return response  # Important: return the response