# middleware.py
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)


class CookieTokenRefreshMiddleware(MiddlewareMixin):
    """
    Middleware to refresh expired access tokens using refresh token.
    Doesn't set request.user - leaves that to DRF authentication classes.
    """

    PUBLIC_PATHS = [
        '/api/v1/auth/',
        '/api/v1/doctors/',
    ]

    def __init__(self, get_response):
        super().__init__(get_response)
        self.access_token_cookie = getattr(settings, 'JWT_ACCESS_COOKIE_NAME', 'access_token')
        self.refresh_token_cookie = getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh_token')
        self.access_token_age = getattr(settings, 'JWT_ACCESS_TOKEN_AGE', 1800)
        self.secure_cookies = getattr(settings, 'JWT_SECURE_COOKIES', not settings.DEBUG)
        self.samesite = getattr(settings, 'JWT_COOKIE_SAMESITE', 'Lax')

    def is_public_path(self, path):
        for public_path in self.PUBLIC_PATHS:
            if path.startswith(public_path):
                return True
        return False

    def process_request(self, request):
        if self.is_public_path(request.path):
            return None

        access_token = request.COOKIES.get(self.access_token_cookie)
        refresh_token = request.COOKIES.get(self.refresh_token_cookie)

        # If no access token but refresh token exists, try to refresh
        if not access_token and refresh_token:
            new_access_token = self.refresh_access_token(refresh_token)
            if new_access_token:
                request.new_access_token = new_access_token

        return None

    def process_response(self, request, response):
        if hasattr(request, 'new_access_token'):
            self.set_access_token_cookie(response, request.new_access_token)
        return response

    def refresh_access_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            return str(refresh.access_token)
        except Exception as e:
            logger.debug(f"Token refresh failed: {str(e)}")
            return None

    def set_access_token_cookie(self, response, access_token):
        response.set_cookie(
            key=self.access_token_cookie,
            value=access_token,
            max_age=self.access_token_age,
            secure=self.secure_cookies,
            httponly=True,
            samesite=self.samesite,
            path='/'
        )






# old works
# import logging
# from django.conf import settings
# from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
# from django.contrib.auth import get_user_model
# import jwt
#
# logger = logging.getLogger(__name__)
# User = get_user_model()
#
#
# class CookieTokenRefreshMiddleware(MiddlewareMixin):
#     """
#     Middleware to refresh expired access tokens using refresh token.
#     Doesn't set request.user - leaves that to DRF authentication classes.
#     """
#
#     PUBLIC_PATHS = [
#         '/api/v1/auth/',
#         '/api/v1/doctors/',
#     ]
#
#     def __init__(self, get_response):
#         super().__init__(get_response)
#         self.access_token_cookie = getattr(settings, 'JWT_ACCESS_COOKIE_NAME', 'access_token')
#         self.refresh_token_cookie = getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh_token')
#         self.access_token_age = getattr(settings, 'JWT_ACCESS_TOKEN_AGE', 300)
#
#     def is_public_path(self, path):
#         for public_path in self.PUBLIC_PATHS:
#             if path.startswith(public_path):
#                 return True
#         return False
#
#     def process_request(self, request):
#         if self.is_public_path(request.path):
#             return None
#
#         access_token = request.COOKIES.get(self.access_token_cookie)
#         refresh_token = request.COOKIES.get(self.refresh_token_cookie)
#
#         # If no access token but refresh token exists, try to refresh
#         if not access_token and refresh_token:
#             new_access_token = self.refresh_access_token(refresh_token)
#             if new_access_token:
#                 request.new_access_token = new_access_token
#
#         return None
#
#     def process_response(self, request, response):
#         if hasattr(request, 'new_access_token'):
#             self.set_access_token_cookie(response, request.new_access_token)
#         return response
#
#     def refresh_access_token(self, refresh_token):
#         try:
#             refresh = RefreshToken(refresh_token)
#             return str(refresh.access_token)
#         except Exception as e:
#             logger.debug(f"Token refresh failed: {str(e)}")
#             return None
#
#     def set_access_token_cookie(self, response, access_token):
#         response.set_cookie(
#             key=self.access_token_cookie,
#             value=access_token,
#             max_age=self.access_token_age,
#             secure=settings.JWT_SECURE_COOKIES,
#             httponly=True,
#             samesite=settings.JWT_COOKIE_SAMESITE,
#             path='/'
#         )