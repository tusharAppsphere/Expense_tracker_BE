from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_api_key.authentication import APIKeyAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CombinedAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Try to authenticate with JWT
        jwt_auth = JWTAuthentication()
        try:
            user, jwt_token = jwt_auth.authenticate(request)
            return (user, jwt_token)
        except AuthenticationFailed:
            pass  # Continue to try API key authentication

        # Try to authenticate with API Key
        api_key_auth = APIKeyAuthentication()
        try:
            user, api_key = api_key_auth.authenticate(request)
            return (user, api_key)
        except AuthenticationFailed:
            pass  # Continue if no valid authentication is found

        return None  # No authentication found
