import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

AUTH_SERVICE_URL = "http://authservice:8000/verify-token/"


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise AuthenticationFailed("Необходим токен аутентификации")

        token = token.split(" ")[1]

        try:
            response = requests.post(AUTH_SERVICE_URL, data={"token": token})
            if response.status_code != 200:
                raise AuthenticationFailed("Токен недействителен")
            user_data = response.json()
            print(user_data)
        except requests.RequestException:
            raise AuthenticationFailed("Ошибка соединения с authservice")

        return user_data, None
